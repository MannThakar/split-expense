# Step 03: Login User

- **Status:** Draft
- **Last updated:** 2026-10-04
- **Depends on:** Step 01, Database Setup (`01_database_setup.md`), which provides accounts and the demo account `demo@spendly.dev` (password `demo1234`). Step 02, Register User (`02_register-user.md`), which creates accounts with lowercase emails and sends new users to the Sign in screen with "Account created. Please sign in."

---

## 1. Overview

People can now create a Spendly account, but the Sign in screen does nothing when they submit it. Registered users have no way into the product, and every later feature (the profile page, recording and managing expenses) needs Spendly to know who the person is.

This step lets a registered user sign in with their email address and password, stay signed in while they move around Spendly, and sign out when they're done. It matters because it is the door to everything personal in the product. It has to be quick for the right person, it must not reveal anything useful to the wrong person, and it must never expose a password.

## 2. Goals and Non-Goals

**Goals**
- A registered user can sign in with one short form and arrive at their profile page.
- Mistakes get one clear message. A wrong email or password gets a single generic message that doesn't reveal whether the email has an account.
- The user stays signed in across pages until they sign out or close the browser.
- The navbar makes it obvious whether the user is signed in, and signing out takes one click.
- Signed-in users are never shown the Sign in or Create your account forms.

**Non-Goals**
- The contents of the profile page (Step 4). In this step it is only the destination after signing in.
- Keeping pages like the profile page private to signed-in users (Step 4 and later).
- "Remember me", password reset, email verification and signing in with outside accounts (Google, Apple, etc.).
- Limiting the number of sign-in attempts, or locking accounts after failures.
- Changing or deleting an account.

## 3. Users and Roles

| Role | Description | Allowed in this step | Not allowed in this step |
|---|---|---|---|
| Visitor | Anyone who is not signed in, with or without an account. | Open the Sign in and Create your account screens. Try to sign in. Sign in successfully if they enter a registered email and its correct password. | Sign in without the correct password. Learn whether a given email has an account by trying to sign in. |
| Signed-in user | Someone who has signed in successfully, including with the demo account. | Move between pages while staying signed in. Sign out. | Open the Sign in or Create your account forms (they are sent to the profile page). Switch to a different account without signing out first. |

## 4. User Scenarios

- **S-1.** As a registered user, I want to sign in with my email and password, so that I can reach my own Spendly account.
- **S-2.** As a user who just registered, I want to sign in straight from the screen I land on, so that I can start using Spendly immediately.
- **S-3.** As a user who mistyped something, I want a clear message and my email still filled in, so that I can try again quickly.
- **S-4.** As a signed-in user, I want to stay signed in as I move around, so that I don't have to sign in on every page.
- **S-5.** As a signed-in user, I want to sign out with one click, so that the next person using this browser can't see my account.
- **S-6.** As an account owner, I want failed sign-ins not to reveal whether my email is registered, so that strangers can't find out I use Spendly.

## 5. Functional Requirements

- **FR-1.** A visitor can reach the Sign in screen from the navbar link "Sign in", from the "Sign in" link in "Already have an account? Sign in" on the Create your account screen, and automatically after registering (Step 02).
- **FR-2.** The Sign in screen shows the heading "Welcome back", the subheading "Sign in to your Spendly account", the fields Email address and Password, a "Sign in" button, and the line "Don't have an account? Create one free", where "Create one free" opens the Create your account screen.
- **FR-3.** The product checks both fields against VR-1 to VR-4 when the form is submitted. If any check fails, it shows exactly one error message at the top of the form card, for Email address first and then Password. It checks the email and password against accounts only after both fields pass.
- **FR-4.** The product finds the account by email, ignoring letter case and spaces at the start and end. The password must match exactly as typed, including letter case and spaces.
- **FR-5.** If the email belongs to an account and the password is correct, the product signs the user in and takes them to the profile page.
- **FR-6.** If the email has no account, or the password is wrong, the product shows the same message, "Incorrect email or password.", and does not sign anyone in.
- **FR-7.** After any rejected attempt, the Sign in screen shows again with the Email address the user typed, and the Password field is empty.
- **FR-8.** Once signed in, the user stays signed in as they open other Spendly pages, until they sign out or close the browser.
- **FR-9.** While a user is signed in, the navbar shows "Sign out" in place of "Get started" and "Sign in". While nobody is signed in, the navbar shows "Get started" and "Sign in" as before.
- **FR-10.** Selecting "Sign out" signs the user out and opens the Sign in screen, which shows "You have been signed out." once.
- **FR-11.** A signed-in user who opens the Sign in or Create your account screen is taken to the profile page instead, and stays signed in as the same account.
- **FR-12.** The product never displays a password, never re-fills the Password field, and never includes a password in any message.

## 6. User Flow and Screens

**Flow: sign in**
1. The visitor selects "Sign in" in the navbar or in "Already have an account? Sign in", or arrives after registering.
2. The **Sign in** screen opens with the cursor in Email address.
3. The visitor enters their email and password and selects **Sign in**.
4. If something is wrong, the same screen shows again with one message at the top. The email is kept and the password is empty. The visitor fixes it and goes back to step 3.
5. If the details are correct, the visitor is signed in and the **profile page** opens. Until Step 4, the profile page is a placeholder.

**Flow: sign out**
1. A signed-in user selects **Sign out** in the navbar on any page that shows the navbar.
2. They are signed out and the **Sign in** screen opens with "You have been signed out."

**Screen: Sign in**
- Heading: "Welcome back"
- Subheading: "Sign in to your Spendly account"
- Message area at the top of the card, only when there is something to say. It shows either an error message in the error style, or one of these success messages in the success style: "Account created. Please sign in." (from Step 02) or "You have been signed out."
- Fields, in order:

| Label | Placeholder | Notes |
|---|---|---|
| Email address | nitish@example.com | Cursor starts here. Kept after an error. |
| Password | Your password | Characters hidden. Always empty when the screen shows. |

- Button: "Sign in"
- Footer line: "Don't have an account? Create one free"

**Navbar**

| State | Shows |
|---|---|
| Not signed in | Spendly logo, "Features", "Get started", "Sign in" |
| Signed in | Spendly logo, "Features", "Sign out" |

**Messages**

| When | Message | Style |
|---|---|---|
| Email blank | "Please enter your email address." | Error |
| Email not a valid address | "Please enter a valid email address." | Error |
| Email too long | "Email must be 254 characters or fewer." | Error |
| Password blank | "Please enter your password." | Error |
| Email has no account, or password wrong | "Incorrect email or password." | Error |
| Spendly can't check the details right now | "We couldn't sign you in right now. Please try again in a moment." | Error |
| After signing out | "You have been signed out." | Success |

## 7. Validation Rules

The product checks these after removing spaces at the start and end of Email address. The password is checked exactly as typed. Lengths count characters as the user sees them, so one emoji counts as one character. There is no minimum or maximum password length here: any non-blank password is compared with the account, and a wrong one gets "Incorrect email or password."

| ID | Field | Required? | Allowed values / format | Min | Max | Message when invalid |
|---|---|---|---|---|---|---|
| VR-1 | Email address | Required | See VR-2 | 1 | 254 | Blank or only spaces: "Please enter your email address." |
| VR-2 | Email address | Required | Same format as Step 02 VR-4: exactly one "@", at least one character before it, a domain after it with at least one dot and text on both sides, and no spaces | n/a | n/a | "Please enter a valid email address." |
| VR-3 | Email address | Required | Same as VR-2 | 1 | 254 | Over 254 characters: "Email must be 254 characters or fewer." |
| VR-4 | Password | Required | Any characters, including spaces and emoji | 1 | n/a | Blank: "Please enter your password." |

## 8. States

| State | What the user sees |
|---|---|
| Empty | The Sign in screen with both fields blank, placeholders showing, the cursor in Email address and no message. |
| Loading | The browser's normal page-loading indicator after "Sign in" is selected. The button and fields look unchanged and there is no custom spinner. |
| Success | The profile page. Any page that shows the navbar now shows "Sign out" and no "Get started" or "Sign in". |
| Error | The Sign in screen with one message in the error style at the top of the card. Email address keeps what was typed and Password is empty. |
| Partial | One field is filled and the other is blank. Submitting shows the message for the first failing field (email first), and the typed email is kept. |
| Disabled | Not applicable. The "Sign in" button and fields are never disabled. Mistakes are reported after submitting. |
| First-time | The same as Empty. A user arriving straight after registering also sees "Account created. Please sign in." in the success style. |
| Signed out | The Sign in screen with "You have been signed out." in the success style, both fields blank, and the navbar showing "Get started" and "Sign in". |

## 9. Error Handling

| ID | Failure | Message shown | How the user recovers |
|---|---|---|---|
| ER-1 | Invalid input in a field | The matching VR message (VR-1 to VR-4) | Fix the field named in the message, re-enter the password and submit again. |
| ER-2 | The email has no account, or the password is wrong | "Incorrect email or password." | Check both, re-enter the password and try again. Select "Create one free" if they have no account. |
| ER-3 | Lost connection before the form reaches Spendly | The browser's own "no internet connection" page. Spendly shows nothing because it never received the form. | Reconnect, go back, re-enter the password and submit again. |
| ER-4 | Timeout, or Spendly temporarily unable to check the details | "We couldn't sign you in right now. Please try again in a moment." | Wait, re-enter the password and submit again. The user is not signed in. |
| ER-5 | Any other unexpected failure while signing in | "We couldn't sign you in right now. Please try again in a moment." | Same as ER-4. The user is never left half signed in. |

"Action not allowed" is not an error in this step: a signed-in user opening the Sign in or Create your account screen is simply taken to the profile page (FR-11). "Something not found" is covered by ER-2, deliberately using the same message as a wrong password. "Duplicate" is covered by EC-4.

## 10. Edge Cases

| ID | Situation | Expected behavior |
|---|---|---|
| EC-1 | Email typed with different letter case or extra spaces, e.g. "  Demo@Spendly.DEV  " | Signs in to demo@spendly.dev when the password is correct. |
| EC-2 | Password differs only in letter case, e.g. "DEMO1234" for the demo account | "Incorrect email or password." |
| EC-3 | Password has an extra space at the start or end that the real password doesn't, e.g. "demo1234 " | "Incorrect email or password." Passwords are never trimmed. |
| EC-4 | Double click on "Sign in", or the form is sent twice quickly | The user ends up signed in once, as that account, on the profile page. No error is shown. |
| EC-5 | Refresh after an error message | The Sign in screen shows again and the user is not signed in. If the browser asks to resend the form, resending counts as a new attempt. |
| EC-6 | Back button after signing in, then submitting the Sign in form again, even with another account's details | The user is taken to the profile page and stays signed in as the original account. |
| EC-7 | Back button after signing out | The browser may show an earlier page from its history. Any page newly opened shows the signed-out navbar, and the user is not signed in. |
| EC-8 | The same account signs in on two browsers or devices | Both are signed in. Signing out on one does not sign out the other. |
| EC-9 | Very long pasted input, e.g. 10,000 characters | In Email address: "Email must be 254 characters or fewer." In Password: "Incorrect email or password." The page still works normally. |
| EC-10 | Input that looks like code, e.g. "' OR 1=1 --" | In Email address: "Please enter a valid email address." In Password: "Incorrect email or password." Nobody is signed in, and anything shown back appears as plain text. |
| EC-11 | Account password with emoji or spaces, e.g. " my pass 😀 " registered in Step 02 | Signs in when the password is typed exactly the same. |
| EC-12 | A field missing from the submission entirely, e.g. from a modified page | Treated as blank, and the matching "Please enter …" message shows. Nobody is signed in. |
| EC-13 | "Sign out" is opened while nobody is signed in, e.g. from an old bookmark | The Sign in screen opens with no message and no error. |
| EC-14 | Many wrong attempts in a row | Each one shows "Incorrect email or password." There is no lockout in this step, and the correct password still works afterwards. |
| EC-15 | User registers, then signs in from the screen showing "Account created. Please sign in." | Signs in normally. The "Account created" message does not appear again after signing out or on later visits. |
| EC-16 | The browser is fully closed and reopened after signing in | The user is signed out. Some browsers that restore previous sessions may keep them signed in. |

## 11. Business Rules and Constraints

- **BR-1.** A failed sign-in never reveals whether an email has an account. An unknown email and a wrong password get exactly the same message.
- **BR-2.** Passwords are never shown, re-filled into a form or included in a message. This continues Step 01 and Step 02.
- **BR-3.** Email matching ignores letter case and spaces at the start and end, matching Step 02's rule that emails are saved in lowercase. Passwords must match exactly.
- **BR-4.** One browser is signed in as at most one account at a time. To use another account, the user signs out first.
- **BR-5.** Signing in and out never changes any account or any expense, including the demo account and its 8 sample expenses.
- **BR-6.** There is no limit on sign-in attempts in this step.
- **BR-7.** Only one error message shows at a time: Email address first, then Password. Account details are checked only after both fields pass.
- **BR-8.** A signed-in user is never shown the Sign in or Create your account forms.

## 12. Acceptance Criteria

- **AC-1** (FR-1). **Given** a visitor on any page with the navbar, **when** they select "Sign in", **then** the Sign in screen opens. **Given** the Create your account screen, **when** they select "Sign in" in the footer line, **then** the Sign in screen opens.
- **AC-2** (FR-2). **Given** the Sign in screen, **when** it loads, **then** it shows "Welcome back", "Sign in to your Spendly account", Email address, Password, the "Sign in" button and "Don't have an account? Create one free". Selecting "Create one free" opens the Create your account screen.
- **AC-3** (FR-3). **Given** both fields are blank, **when** the form is submitted, **then** only "Please enter your email address." is shown.
- **AC-4** (FR-4). **Given** the demo account, **when** a visitor signs in with "  DEMO@spendly.dev  " and "demo1234", **then** they are signed in as the demo account.
- **AC-5** (FR-5). **Given** the demo account, **when** a visitor signs in with "demo@spendly.dev" and "demo1234", **then** the profile page opens and the navbar on later pages shows "Sign out".
- **AC-6** (FR-6). **Given** "nobody@example.com" has no account, **when** someone signs in with it, **then** they see "Incorrect email or password.", exactly the same as for the demo email with the password "wrongpass1".
- **AC-7** (FR-7). **Given** any rejected attempt, **when** the Sign in screen shows again, **then** Email address keeps what was typed and Password is empty.
- **AC-8** (FR-8). **Given** a signed-in user, **when** they open the landing, Terms and Privacy pages, **then** each one shows them as signed in.
- **AC-9** (FR-9). **Given** nobody is signed in, **when** any page with the navbar loads, **then** it shows "Get started" and "Sign in" and no "Sign out". **Given** a signed-in user, **then** it shows "Sign out" and neither "Get started" nor "Sign in".
- **AC-10** (FR-10). **Given** a signed-in user, **when** they select "Sign out", **then** the Sign in screen shows "You have been signed out.", the navbar shows "Get started" and "Sign in", and a refresh removes the message.
- **AC-11** (FR-11). **Given** a signed-in user, **when** they open the Sign in or Create your account screen, **then** the profile page opens and they are still signed in as the same account.
- **AC-12** (FR-12). **Given** any sign-in attempt, successful or not, **when** the user looks at any screen or message, **then** the password never appears and the Password field is never pre-filled.

## 13. Test Cases

Demo account: `demo@spendly.dev` / `demo1234`. "Ana" means an account registered through Step 02 as Ana Silva / ana@example.com / Secret123 unless stated otherwise.

| ID | Type | Linked to | Preconditions | Steps | Test data | Expected result |
|---|---|---|---|---|---|---|
| TC-1 | Happy path | FR-5, AC-5 | Signed out | Open Sign in, enter details, select Sign in, then open the landing page | demo@spendly.dev / demo1234 | The profile page opens. The landing page navbar shows "Sign out" and no "Get started" or "Sign in". |
| TC-2 | Happy path | FR-1, FR-2, AC-1, AC-2 | Signed out | Select "Sign in" in the navbar. Select "Create one free". On Create your account, select "Sign in". | n/a | The navbar link opens Sign in, showing "Welcome back", "Sign in to your Spendly account", Email address, Password, the "Sign in" button and "Don't have an account? Create one free". "Create one free" opens Create your account. Its "Sign in" link opens Sign in. |
| TC-3 | Happy path | FR-9, FR-10, AC-9, AC-10 | Signed in as demo | Select "Sign out", then refresh | n/a | Sign in shows "You have been signed out." in the success style. The navbar shows "Get started" and "Sign in". After the refresh the message is gone. |
| TC-4 | Happy path | FR-8, AC-8 | Signed in as demo | Open the landing, Terms and Privacy pages in turn | n/a | Each page's navbar shows "Sign out". |
| TC-5 | Validation | VR-1, ER-1 | Signed out | Submit with email blank, then valid | "" ; demo@spendly.dev (password demo1234) | Blank shows "Please enter your email address." The valid email signs in and opens the profile page. |
| TC-6 | Validation | VR-2, ER-1 | Signed out | Submit invalid email, then valid | "demo.spendly.dev" ; demo@spendly.dev (password demo1234) | Invalid shows "Please enter a valid email address." The valid email signs in. |
| TC-7 | Validation | VR-3, ER-1 | Signed out | Submit long email, then valid | 255 characters (`a`×243 + "@example.com") ; demo@spendly.dev | 255 characters shows "Email must be 254 characters or fewer." The valid email signs in. |
| TC-8 | Validation | VR-4, ER-1 | Signed out | Submit with password blank, then filled | demo@spendly.dev with "" ; "demo1234" | Blank shows "Please enter your password." "demo1234" signs in. |
| TC-9 | Validation | FR-3, AC-3, BR-7 | Signed out | Submit with both fields blank. Then submit an invalid email with a blank password. | "" / "" ; "abc" / "" | First: only "Please enter your email address." Second: only "Please enter a valid email address." |
| TC-10 | Boundary | VR-1, VR-3 | Signed out. No accounts with these emails. | Submit emails of each length with password "Secret123" | 1 character "a"; 253; 254; 255 characters (padding before "@example.com") | "a" shows "Please enter a valid email address." 253 and 254 show "Incorrect email or password." (accepted by validation, no account). 255 shows "Email must be 254 characters or fewer." |
| TC-11 | Boundary | VR-4, FR-4 | Signed out. An account registered with a 128-character password of "x" | Sign in with passwords of each length | 0; 1 ("x"); 127; 128; 129 characters of "x" | 0 shows "Please enter your password." 1, 127 and 129 show "Incorrect email or password." 128 signs in. |
| TC-12 | Error | ER-1, FR-7, AC-7 | Signed out | Submit an invalid email | "demo@spendly" / demo1234 | "Please enter a valid email address." Email address still shows "demo@spendly". Password is empty. Not signed in. |
| TC-13 | Error | ER-2, FR-6, FR-7, FR-12, AC-6, AC-7, AC-12 | Signed out | Submit the demo email with a wrong password | demo@spendly.dev / wrongpass1 | "Incorrect email or password." Email kept, Password empty, "wrongpass1" appears nowhere on the page. Not signed in. |
| TC-14 | Error | ER-2, FR-6, BR-1, AC-6 | Signed out. No account for the email. | Submit an unknown email | nobody@example.com / wrongpass1 | Exactly "Incorrect email or password.", identical to TC-13. Not signed in. |
| TC-15 | Error | ER-3 | Signed out. Browser offline. | Select Sign in | demo@spendly.dev / demo1234 | The browser shows its offline page and the user is not signed in. After reconnecting and resubmitting, the profile page opens. |
| TC-16 | Error | ER-4 | Spendly made temporarily unable to check details | Submit valid details | demo@spendly.dev / demo1234 | "We couldn't sign you in right now. Please try again in a moment." Email kept, Password empty, not signed in. After recovery, submitting again signs in. |
| TC-17 | Error | ER-5 | An unexpected failure is forced during sign-in | Submit valid details | demo@spendly.dev / demo1234 | The same message as TC-16. The navbar still shows "Get started" and "Sign in". |
| TC-18 | Empty / missing | FR-2 | Signed out, first visit | Open Sign in | n/a | Both fields blank with placeholders "nitish@example.com" and "Your password". Cursor in Email address. No message. |
| TC-19 | Empty / missing | VR-4, FR-7 | Signed out | Fill only the email and submit | demo@spendly.dev / "" | "Please enter your password." Email address still shows demo@spendly.dev. |
| TC-20 | Empty / missing | EC-12 | Signed out | Send the form with the Password field missing entirely | email demo@spendly.dev only | "Please enter your password." Not signed in. |
| TC-21 | Edge case | EC-1, FR-4, AC-4 | Signed out | Sign in with mixed case and spaces | "  Demo@Spendly.DEV  " / demo1234 | Signed in as the demo account. Profile page opens. |
| TC-22 | Edge case | EC-2 | Signed out | Sign in with a different-case password | demo@spendly.dev / DEMO1234 | "Incorrect email or password." |
| TC-23 | Edge case | EC-3 | Signed out | Sign in with a trailing space on the password | demo@spendly.dev / "demo1234 " | "Incorrect email or password." |
| TC-24 | Edge case | EC-4 | Signed out | Double click "Sign in" | demo@spendly.dev / demo1234 | The profile page opens with no error, signed in as demo. |
| TC-25 | Edge case | EC-5 | Wrong-password error showing | Refresh and accept the browser's resend prompt | demo@spendly.dev / wrongpass1 | "Incorrect email or password." again. Not signed in. |
| TC-26 | Edge case | EC-6, BR-4 | Signed in as demo. Ana registered. | Go back to the Sign in page in history and submit Ana's details | ana@example.com / Secret123 | The profile page opens. The user is still signed in as demo, not Ana. |
| TC-27 | Edge case | EC-7 | Signed in, then signed out | Press Back, then open the landing page | n/a | The landing page navbar shows "Get started" and "Sign in". Not signed in. |
| TC-28 | Edge case | EC-8 | Two separate browsers | Sign in as demo in both, then sign out in browser A and refresh browser B | demo@spendly.dev / demo1234 | Browser A is signed out. Browser B still shows "Sign out" in the navbar. |
| TC-29 | Edge case | EC-9 | Signed out | Paste 10,000 characters into Email address, then into Password (with demo email) | 10,000 × "a" | Email: "Email must be 254 characters or fewer." Password: "Incorrect email or password." The page responds normally. |
| TC-30 | Edge case | EC-10 | Signed out | Submit code-like input in each field | Email "' OR 1=1 --" ; demo@spendly.dev with password "' OR 1=1 --" | Email: "Please enter a valid email address.", with the text shown as typed. Password: "Incorrect email or password." Not signed in. |
| TC-31 | Edge case | EC-11 | Signed out. Account registered with password " my pass 😀 " | Sign in with that exact password | ben@example.com / " my pass 😀 " | Signed in. Profile page opens. |
| TC-32 | Edge case | EC-13 | Signed out | Open the Sign out link directly | n/a | The Sign in screen opens with no message and no error. |
| TC-33 | Edge case | EC-14, BR-6 | Signed out | Submit a wrong password 10 times, then the correct one | demo@spendly.dev / wrongpass1 ×10, then demo1234 | Each wrong attempt shows "Incorrect email or password." The 11th attempt signs in. |
| TC-34 | Edge case | EC-15 | Signed out | Register a new account, sign in from the next screen, sign out | Cara / cara@example.com / Secret123 ×2 | Sign in shows "Account created. Please sign in." Signing in opens the profile page. After signing out, only "You have been signed out." is shown. |
| TC-35 | Edge case | EC-16 | Signed in as demo. Browser set not to restore sessions. | Fully close the browser, reopen it, open the landing page | n/a | The navbar shows "Get started" and "Sign in". |
| TC-36 | Permission | Visitor role, FR-1 | Signed out | Open Sign in, then Create your account | n/a | Both forms show normally. |
| TC-37 | Permission | FR-11, AC-11, BR-8 | Signed in as demo | Open the Sign in screen directly | n/a | The profile page opens. Still signed in as demo. |
| TC-38 | Permission | FR-11, AC-11, BR-8 | Signed in as demo | Open the Create your account screen directly | n/a | The profile page opens. No form is shown and no account can be created. |
| TC-39 | Regression | Step 02 FR-6, FR-7, FR-9 | Signed out | Register, then sign in with the email in different letter case | Dev / Dev.User@Example.COM / Secret123 ×2, then dev.user@example.com / Secret123 | Registration shows "Account created. Please sign in." Signing in opens the profile page. |
| TC-40 | Regression | Step 02 ER-2, FR-11 | Signed out | Register an existing email, then register a new one | demo@spendly.dev ; eve@example.com | The first shows "An account with this email already exists. Please sign in instead." The second succeeds, and the navbar still shows "Get started" and "Sign in" (registering does not sign in). |
| TC-41 | Regression | Step 01 FR-4, BR-5 | Demo account with its 8 sample expenses | Sign in and out as demo three times | demo@spendly.dev / demo1234 | The demo account still exists with the same name and the same 8 expenses. |
| TC-42 | Regression | FR-9 | Signed out, then signed in | Open the Terms and Privacy pages in each state | n/a | Both pages open in both states, with the navbar matching the state (FR-9) and the footer links unchanged. |

## 14. Out of Scope

- The contents of the profile page (Step 4).
- Making pages like the profile page available only to signed-in users (Step 4 and later).
- Recording, editing and deleting expenses (Steps 7 to 9).
- "Remember me", staying signed in after the browser closes, and automatic sign-out after inactivity.
- Password reset, email verification and signing in with outside accounts.
- Limiting sign-in attempts and locking accounts.
- Showing the user's name in the navbar.

## 15. Assumptions and Open Questions

**Decisions from the developer**
- A successful sign-in goes to the profile page.
- Signing out is part of this step, and the navbar changes while signed in.
- A wrong email or password gets one generic message: "Incorrect email or password."
- A signed-in user who opens Sign in or Create your account is sent to the profile page. This answers Step 02's OQ-3.

**Assumptions (defaults chosen)**
- Signing out leads to the Sign in screen with "You have been signed out."
- The user stays signed in until they sign out or close the browser. There is no time limit.
- Email checks reuse Step 02's format and 254-character limit. Password has no length rules at sign-in, so any non-blank value is compared.
- Only the email is kept after an error. The password is always cleared.
- The browser's own "please fill in this field" prompt may appear before Spendly's message for blank fields. This is acceptable, and Spendly's message still shows if a blank reaches it.
- The signed-in navbar keeps "Features" and shows only "Sign out" next to it.
- Existing specs are in `.claude/specs/` as `NN_name.md`, so this spec follows that pattern rather than `specs/NN-name/spec.md`.

**Open questions**
- **OQ-1.** Should the navbar show the signed-in user's name (e.g. "Hi, Ana") next to "Sign out"?
- **OQ-2.** Should repeated failed sign-ins be limited or slowed down to protect accounts? This step deliberately has no limit (BR-6).
- **OQ-3.** Until Step 4 makes the profile page private, someone who is not signed in can still open it directly and see its placeholder. Is that acceptable for now?
- **OQ-4.** Should Spendly offer "Remember me" so users stay signed in after closing the browser?
