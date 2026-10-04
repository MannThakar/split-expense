import os

import psycopg2
import psycopg2.errors
import psycopg2.extras
from werkzeug.security import generate_password_hash

CATEGORIES = ["Food", "Transport", "Bills", "Health", "Entertainment", "Shopping", "Other"]

_categories_sql = ", ".join(f"'{c}'" for c in CATEGORIES)  # hardcoded constant, not user input

CREATE_USERS_SQL = """
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
"""

CREATE_EXPENSES_SQL = f"""
CREATE TABLE IF NOT EXISTS expenses (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    amount NUMERIC(10,2) NOT NULL,
    category TEXT NOT NULL CHECK (category IN ({_categories_sql})),
    date DATE NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
"""

# Emails are saved lowercase; this also enforces case-insensitive uniqueness
# for any future path that creates users.
CREATE_EMAIL_LOWER_INDEX_SQL = """
CREATE UNIQUE INDEX IF NOT EXISTS users_email_lower_idx ON users (LOWER(email));
"""

DEMO_EMAIL = "demo@spendly.dev"


class EmailTakenError(Exception):
    """Raised by create_user when the email already belongs to an account."""
DEMO_PASSWORD = "demo1234"


def get_db():
    """Returns a new connection. Caller must commit/rollback and close it:

        conn = get_db()
        try:
            ...
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
    """
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        port=os.environ.get("DB_PORT", "5432"),
        dbname=os.environ.get("DB_NAME", "expense_tracker"),
        user=os.environ.get("DB_USER", "postgres"),
        password=os.environ.get("DB_PASSWORD", "123mann4567"),
        cursor_factory=psycopg2.extras.RealDictCursor,
    )


def init_db():
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute(CREATE_USERS_SQL)
            cur.execute(CREATE_EXPENSES_SQL)
            cur.execute(CREATE_EMAIL_LOWER_INDEX_SQL)
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def seed_db():
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM users WHERE email = %s", (DEMO_EMAIL,))
            if cur.fetchone():
                return  # already seeded

            cur.execute(
                "INSERT INTO users (name, email, password_hash) VALUES (%s, %s, %s) RETURNING id",
                ("Demo User", DEMO_EMAIL, generate_password_hash(DEMO_PASSWORD)),
            )
            user_id = cur.fetchone()["id"]

            demo_expenses = [
                (user_id, 12.50, "Food", "2026-09-01", "Lunch"),
                (user_id, 45.00, "Transport", "2026-09-02", "Train pass"),
                (user_id, 120.00, "Bills", "2026-09-03", "Electricity"),
                (user_id, 60.00, "Health", "2026-09-05", "Pharmacy"),
                (user_id, 30.00, "Entertainment", "2026-09-07", "Cinema"),
                (user_id, 75.25, "Shopping", "2026-09-10", "New shoes"),
                (user_id, 15.00, "Other", "2026-09-12", "Misc"),
                (user_id, 22.00, "Food", "2026-09-15", "Groceries"),
            ]
            cur.executemany(
                "INSERT INTO expenses (user_id, amount, category, date, description) "
                "VALUES (%s, %s, %s, %s, %s)",
                demo_expenses,
            )
        conn.commit()
    except psycopg2.errors.UniqueViolation:
        conn.rollback()  # concurrent instance won the seeding race — not an error
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def create_user(name, email, password):
    """Creates a user and returns its id. Expects a trimmed name and a
    lowercased email; raises EmailTakenError if the email is already used."""
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO users (name, email, password_hash) VALUES (%s, %s, %s) RETURNING id",
                (name, email, generate_password_hash(password)),
            )
            user_id = cur.fetchone()["id"]
        conn.commit()
        return user_id
    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        raise EmailTakenError(email)
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
