# Spec: Database Setup (Schema, Connection, Seed Data)

## 1. Problem Statement / Overview

**Why:** The app has no database yet. Authentication, profile and expense tracking all need a place to store users and their expenses.

**Who is affected:** Every future feature, and every developer running the app locally.

**Current behavior:** There is no schema, no shared way to connect, and no sample data. Features cannot be built or tested against real data.

**Why insufficient:** Without one shared and correct data layer, each feature would connect in its own way and define data in its own way. That leads to inconsistent data, missing rules and security risks.

**Expected outcome:** When the app starts, the database is ready. The `users` and `expenses` tables exist with the agreed columns and rules, and a small set of demo data exists exactly once. All code gets its database connection through a single `get_db` function.

---

## 2. Functional Requirements

**FR-1 Connection (`get_db`)**

- `database/db.py` provides `get_db`, which returns a working connection to the local PostgreSQL database.
- It is the only way application code obtains a database connection.
- Connections are always released after use. None are left open after a request finishes, even when that request fails.
- Query results can be read by column name.

**FR-2 Table setup (`init_db`)**

- `init_db` makes sure the `users` and `expenses` tables exist with the structure in FR-3.
- It is safe to run any number of times. It never errors because the tables already exist, and it never removes or changes existing data.

**FR-3 Data structure**

**users**

| Column        | Meaning                   | Rules                                               |
| ------------- | ------------------------- | --------------------------------------------------- |
| id            | Unique user identifier    | Primary key, generated automatically, never reused  |
| name          | Display name              | Required                                            |
| email         | Login email               | Required, unique across all users                   |
| password_hash | Hashed password           | Required, never the plain password                  |
| created_at    | When the user was created | Filled automatically with the current date and time |

**expenses**

| Column      | Meaning                     | Rules                                               |
| ----------- | --------------------------- | --------------------------------------------------- |
| id          | Unique expense identifier   | Primary key, generated automatically, never reused  |
| user_id     | Owner of the expense        | Required, must refer to an existing user            |
| amount      | Money spent                 | Required, decimal number (not a whole number)       |
| category    | Expense category            | Required, one of the fixed categories (FR-5)        |
| date        | Day the expense happened    | Required, YYYY-MM-DD                                |
| description | Optional note               | May be empty                                        |
| created_at  | When the record was created | Filled automatically with the current date and time |

**FR-4 Demo data (`seed_db`)**

- `seed_db` inserts one demo user and 8 demo expenses belonging to that user. Together the expenses use all 7 categories.
- The demo user's password is stored only as a hash made with `werkzeug.security.generate_password_hash`.
- Running `seed_db` again never creates duplicates. If the demo data is already there, nothing is inserted and no error is raised.
- Seeding is all-or-nothing. If any part fails, no partial demo data remains.

**FR-5 Categories (fixed list)**
Only these exact values are valid: `Food`, `Transport`, `Bills`, `Health`, `Entertainment`, `Shopping`, `Other`. The list is defined in one place so that future features reuse it.

**FR-6 App startup**

- `app.py` imports `get_db`, `init_db` and `seed_db`.
- When the app starts, it runs table setup and then demo data, before it serves any request.

---

## 3. API Contracts

API contract is not applicable for this feature. No HTTP endpoints are added.

---

## 4. Constraints

- The database is a local PostgreSQL instance.
- No ORM (no SQLAlchemy).
- Parameterized queries only. SQL is never built with string formatting.
- Foreign-key rules are enforced on every connection.
- `amount` is stored as a decimal number, not an integer.
- Passwords are hashed with `werkzeug.security.generate_password_hash`.
- Dates follow YYYY-MM-DD everywhere they are stored or read.
- Changes to `app.py` are additions only. Existing behavior must not break.
- No unnecessary new dependencies.
- Database credentials must not appear in error messages or logs.

---

## 5. Edge Cases and Error Handling

| Case                                                                       | Expected behavior                                                                                   |
| -------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| Database is unreachable or credentials are wrong                           | Startup stops with a clear error saying the database can't be reached. The password is never shown. |
| Tables already exist                                                       | Setup succeeds and no data changes.                                                                 |
| App restarted, or `seed_db` run again                                      | No duplicate demo data.                                                                             |
| Demo data removed manually, then app restarted                             | Demo data is created again.                                                                         |
| Seeding fails partway                                                      | No partial demo data remains, and the error is reported.                                            |
| A new user uses an email that already exists                               | Rejected.                                                                                           |
| An expense refers to a user that doesn't exist                             | Rejected.                                                                                           |
| An expense uses a category outside the list, including wrong case (`food`) | Rejected.                                                                                           |
| A date is invalid or in the wrong format (`2026-02-30`, `29/09/2026`)      | Rejected.                                                                                           |
| Amount is missing                                                          | Rejected.                                                                                           |
| Description is missing or empty                                            | Accepted.                                                                                           |
| Input containing SQL-like text (`' OR 1=1 --`)                             | Stored as plain text and never executed.                                                            |
| A request fails midway                                                     | Its connection is still released, and no half-finished changes are saved.                           |
| Two app instances start at the same time                                   | There is still only one set of demo data, and neither instance crashes.                             |

---

## 6. Acceptance Criteria

1. Starting the app against an empty database creates the `users` and `expenses` tables with the columns and rules in FR-3.
2. After the first start there is 1 demo user and 8 demo expenses, and together the expenses cover all 7 categories.
3. After restarting the app 3 times, the demo user count is still 1 and the demo expense count is still 8.
4. The demo user's stored password is a hash, and it verifies against the demo password using werkzeug.
5. Every stored expense date reads back in YYYY-MM-DD format.
6. An expense for a non-existent user is rejected.
7. An expense with a category outside the fixed list is rejected.
8. A second user with an existing email is rejected.
9. An expense with an invalid date is rejected.
10. A stored amount such as 12.50 reads back as a decimal value, not a whole number.
11. When the database is unreachable, startup fails with a readable error that doesn't show the password.
12. No SQL in `database/db.py` or `app.py` is built with string formatting.
13. No ORM is used.

---

## Specification Review

### Covered

- The problem and why it matters.
- The data structure and its rules.
- The three functions and when they run at startup.
- The fixed categories.
- Seeding that never creates duplicates.
- Password hashing.
- Query safety.
- Error cases.
- Testable acceptance criteria.

### Missing

- Future schema changes: `init_db` only creates missing tables. It won't add columns to existing ones, so later features such as profile may need a way to change the schema. That is out of scope here.

### Ambiguous

- None that block this spec. The technical choices are deferred to plan mode.

### Risks

- **Demo account in production:** if seeding runs in every environment, production gets a demo login whose password is known. Worth deciding before this goes to production.
- **Rounding in totals:** amounts stored as decimal numbers can round in totals later, when expense reports add them up. The plan should pick a storage type that keeps cents exact.

### Recommendation

Ready for approval. Once you approve it, the next step is the Implementation Plan.
