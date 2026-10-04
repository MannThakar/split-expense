# Step 02: Register User

- **Status:** Draft
- **Last updated:** 2026-10-04
- **Depends on:** Step 01, Database Setup (`01_database_setup.md`). Step 01 provides account storage with one account per email, password protection, and the sample demo account `demo@spendly.dev` with its 8 sample expenses. The existing screens are also needed: the landing page, the "Create your account" screen and the Sign in screen.

---

## 1. Overview

People who arrive at Spendly can read the landing page and see a "Create your account" screen, but submitting that screen does nothing yet. Every later feature (signing in, a profile, recording expenses) needs the person to have an account first.

This step lets a first-time visitor create a Spendly account with their full name, email address and a password. Afterwards they are sent to the Sign in screen. The step matters because it is how people start using the product. It needs to be quick, it needs to explain mistakes clearly, and it needs to keep passwords safe.

## 2. Goals and Non-Goals

**Goals**
- A visitor can create an account in one short form and know right away whether it worked.
- Every mistake gets one clear, specific message. Anything the visitor typed, apart from passwords, is kept so they can fix it quickly.
- Only one account can exist for each email address, whatever the letter case.
- Passwords are never shown back, never re-filled into the form and never kept in readable form.

**Non-Goals**
- Signing in, staying signed in, or signing out. These come in later steps.
- Email verification, welcome emails or password reset.
- Signing up with Google, Apple or another outside account.
- Editing or deleting an account.
- Password strength meters or rules about character types.

## 3. Users and Roles

| Role | Description | Allowed in this step | Not allowed in this step |
|---|---|---|---|
| Visitor | Anyone without a Spendly account. | Open the "Create your account" screen and create one account with an email that is not in use yet. | Create an account with an email that is already registered. |
| Registered user | Someone who already has an account, including the demo account. They are not signed in yet because sign-in does not exist. | Open the "Create your account" screen and register a *different* email. | Register their own email again. They are not signed in after registering. |

## 4. User Scenarios

- **S-1.** As a visitor, I want to create an account with my name, email and password, so that I can start tracking my expenses.
- **S-2.** As a visitor who made a typo, I want a clear message telling me what to fix, without retyping my name and email, so that I can finish quickly.
- **S-3.** As a visitor who already has an account, I want to be told my email is already registered, so that I go to Sign in instead of making a duplicate.
- **S-4.** As a visitor, I want to confirm my password, so that a typo doesn't lock me out of my new account.
- **S-5.** As a new user, I want to land on the Sign in screen with a confirmation, so that I know my account exists and what to do next.

## 5. Functional Requirements

- **FR-1.** The visitor can reach the "Create your account" screen from the navbar link "Get started", the landing page buttons "Start tracking free" and "Create free account", and the Sign in screen link "Create one free".
- **FR-2.** The "Create your account" screen shows four fields (Full name, Email address, Password, Confirm password), a "Create account" button, and the line "Already have an account? Sign in", where "Sign in" opens the Sign in screen.
- **FR-3.** The product checks every field against rules VR-1 to VR-10 when the form is submitted. If any check fails, it shows exactly one error message at the top of the form card, for the first failing field in this order: Full name, Email address, Password, Confirm password.
- **FR-4.** If a submission is rejected for any reason, the product shows the form again with the Full name and Email address the visitor entered, clears both password fields, and creates no account.
- **FR-5.** The product rejects an email that already belongs to an account, ignoring letter case, and shows the duplicate message (ER-2).
- **FR-6.** If every field is valid and the email is not in use, the product creates exactly one account with the entered name, email and password.
- **FR-7.** After the account is created, the product takes the user to the Sign in screen, which shows the message "Account created. Please sign in." once.
- **FR-8.** The product removes spaces at the start and end of the Full name and Email address before checking and saving them. Passwords are used exactly as typed.
- **FR-9.** The product saves the email in lowercase, so later sign-in works whatever letter case the user types.
- **FR-10.** The product never displays a password, never re-fills a password field, and never keeps a password in readable form.
- **FR-11.** Creating an account does not sign the user in. After registering, the navbar still shows "Get started" and "Sign in".

## 6. User Flow and Screens

**Flow**
1. The visitor selects "Get started", "Start tracking free", "Create free account" or "Create one free".
2. The **Create your account** screen opens with the cursor in Full name.
3. The visitor fills in the four fields and selects **Create account**.
4. If something is wrong, the same screen shows again with one error message at the top. Name and email are kept and both password fields are empty. The visitor fixes the problem and goes back to step 3.
5. If everything is valid, the account is created and the **Sign in** screen opens with the success message.

**Screen: Create your account**
- Heading: "Create your account"
- Subheading: "Start tracking your expenses today"
- Error area (only when there is an error): one message in the error style at the top of the card.
- Fields, in order:

| Label | Placeholder | Notes |
|---|---|---|
| Full name | Nitish Kumar | Cursor starts here |
| Email address | nitish@example.com | |
| Password | Min. 8 characters | Characters hidden |
| Confirm password | Re-enter your password | Characters hidden |

- Button: "Create account"
- Footer line: "Already have an account? Sign in"

**Screen: Sign in (after success)**
- The existing Sign in screen, plus a success message at the top of the card: "Account created. Please sign in."
- The message shows only on the first visit right after registering. It is not shown again after a refresh.

## 7. Validation Rules

The product checks these after removing spaces at the start and end of Full name and Email address (FR-8). Lengths count characters as the user sees them, so one emoji counts as one character.

| ID | Field | Required? | Allowed values / format | Min | Max | Message when invalid |
|---|---|---|---|---|---|---|
| VR-1 | Full name | Required | Any characters, including letters with accents, apostrophes, hyphens and emoji | 1 | 100 | Blank or only spaces: "Please enter your full name." |
| VR-2 | Full name | Required | Same as VR-1 | 1 | 100 | Over 100 characters: "Name must be 100 characters or fewer." |
| VR-3 | Email address | Required | See VR-4 | 1 | 254 | Blank or only spaces: "Please enter your email address." |
| VR-4 | Email address | Required | Exactly one "@", at least one character before it, a domain after it that contains at least one dot with text on both sides, and no spaces | n/a | n/a | "Please enter a valid email address." |
| VR-5 | Email address | Required | Same as VR-4 | 1 | 254 | Over 254 characters: "Email must be 254 characters or fewer." |
| VR-6 | Password | Required | Any characters, including spaces and emoji. No character-type rules | 8 | 128 | Blank: "Please enter a password." |
| VR-7 | Password | Required | Same as VR-6 | 8 | 128 | Fewer than 8 characters: "Password must be at least 8 characters." |
| VR-8 | Password | Required | Same as VR-6 | 8 | 128 | More than 128 characters: "Password must be 128 characters or fewer." |
| VR-9 | Confirm password | Required | Any | 1 | n/a | Blank, when the password itself is valid: "Please confirm your password." |
| VR-10 | Confirm password | Required | Must match Password exactly, including letter case and spaces | n/a | n/a | "Passwords do not match." |

## 8. States

| State | What the user sees |
|---|---|
| Empty | The Create your account screen with all four fields blank, placeholders showing, the cursor in Full name and no message. |
| Loading | The browser's normal page-loading indicator after "Create account" is selected. The button and fields look unchanged and there is no custom spinner. |
| Success | The Sign in screen with "Account created. Please sign in." at the top of the card. |
| Error | The Create your account screen with one message in the error area at the top of the card. Full name and Email address are kept and both password fields are empty. |
| Partial | Some fields are filled and others are blank. Submitting shows the message for the first failing field (FR-3), and whatever was typed into Full name and Email address is kept. |
| Disabled | Not applicable. The "Create account" button and the fields are never disabled. Mistakes are reported after submitting, not by blocking the button. |
| First-time | The same as Empty. There is no welcome tour or tip. |

## 9. Error Handling

| ID | Failure | Message shown | How the user recovers |
|---|---|---|---|
| ER-1 | Invalid input in any field | The matching VR message (VR-1 to VR-10) | Fix the field named in the message, re-enter both passwords and submit again. |
| ER-2 | Duplicate: the email already belongs to an account (any letter case) | "An account with this email already exists. Please sign in instead." | Select "Sign in" in the footer line, or enter a different email, re-enter both passwords and submit again. |
| ER-3 | Lost connection before the submission reaches Spendly | The browser's own "no internet connection" page. Spendly shows nothing because it never received the form. | Reconnect, go back, re-enter both passwords and submit. If the account was in fact created, the new attempt shows ER-2 and the user signs in. |
| ER-4 | Timeout or Spendly temporarily unable to save | "We couldn't create your account right now. Please try again in a moment." | Wait, re-enter both passwords and submit again. No account was created. |
| ER-5 | Any other unexpected failure while creating the account | "We couldn't create your account right now. Please try again in a moment." | Same as ER-4. No partial or half-created account remains. |

"Action not allowed" and "something not found" do not apply in this step. Nobody is signed in, so no role is blocked from the screen, and there is nothing for the visitor to look up.

## 10. Edge Cases

| ID | Situation | Expected behavior |
|---|---|---|
| EC-1 | Spaces at the start or end of Full name or Email address, e.g. "  Ana Silva  " | Spaces are removed and the account is saved as "Ana Silva". A name made only of spaces shows "Please enter your full name." |
| EC-2 | Name with accents, apostrophes, hyphens or emoji, e.g. "José O'Brien-Núñez 😀" | Accepted and saved exactly as typed (after FR-8). |
| EC-3 | Email differs from an existing account only in letter case, e.g. "Demo@Spendly.DEV" | Rejected with ER-2. |
| EC-4 | Email with a plus sign, dots or a multi-part domain, e.g. "ana.silva+spend@mail.example.co.uk" | Accepted. |
| EC-5 | Password with spaces at the start or end, or emoji, e.g. " my pass 😀 " | Accepted exactly as typed. The spaces count towards the length and must also be in Confirm password. |
| EC-6 | Password and Confirm password differ only in letter case ("Secret123" / "secret123") | "Passwords do not match." |
| EC-7 | Double click on "Create account", or the form is sent twice quickly | Exactly one account is created. If the second submission is processed, the user sees ER-2 and can sign in with the account that was created. |
| EC-8 | Refresh after an error message | The form shows again with no account created. If the browser asks to resend the form, resending behaves like a normal new submission. |
| EC-9 | Refresh on the Sign in screen after success | The Sign in screen shows without the success message, and no second account is created. |
| EC-10 | Back button after a successful registration, then submitting again with the same email | The Create your account screen shows. Resubmitting shows ER-2. |
| EC-11 | Two people register the same email at almost the same moment | Exactly one account is created. The other person sees ER-2. |
| EC-12 | Very long pasted input, e.g. 10,000 characters in Full name | "Name must be 100 characters or fewer." The page still works normally. |
| EC-13 | Malformed emails: "ana@", "@example.com", "ana@example", "ana silva@example.com", "ana@@example.com" | "Please enter a valid email address." |
| EC-14 | Name that looks like markup or code, e.g. "<b>Ana</b>" or "' OR 1=1 --" | Accepted. Wherever the name appears, it shows as literal text with no formatting or other effect. |
| EC-15 | A field missing from the submission entirely, e.g. a modified page that sends no Confirm password | Treated as blank, and the matching "Please …" message shows. No account is created. |
| EC-16 | Registering the demo account email "demo@spendly.dev" | Rejected with ER-2. The demo account is unchanged. |
| EC-17 | Password is the same as the user's email or name | Accepted. There are no password-content rules in this step. |

## 11. Business Rules and Constraints

- **BR-1.** One account per email address, ignoring letter case. This builds on Step 01's rule that emails are unique.
- **BR-2.** Passwords are never kept in readable form, never shown, never re-filled into a form and never included in any message. This matches Step 01.
- **BR-3.** Emails are saved in lowercase. Names are saved as typed, apart from spaces at the start and end.
- **BR-4.** Anyone can register. There is no invite, approval or email verification in this step.
- **BR-5.** A new account starts with no expenses.
- **BR-6.** Registering never signs the user in.
- **BR-7.** Registering never changes or removes any existing account, including the demo account and its sample expenses.
- **BR-8.** Only one error message is shown at a time, in field order: Full name, Email address, Password, Confirm password. The duplicate-email check runs after all field checks pass.

## 12. Acceptance Criteria

- **AC-1** (FR-1). **Given** a visitor on the landing page, **when** they select "Get started", "Start tracking free" or "Create free account", **then** the Create your account screen opens. **Given** a visitor on the Sign in screen, **when** they select "Create one free", **then** the Create your account screen opens.
- **AC-2** (FR-2). **Given** the Create your account screen, **when** it loads, **then** it shows the fields Full name, Email address, Password and Confirm password, the "Create account" button, and "Already have an account? Sign in". Selecting "Sign in" opens the Sign in screen.
- **AC-3** (FR-3). **Given** a form where both Full name and Password are invalid, **when** it is submitted, **then** only "Please enter your full name." is shown.
- **AC-4** (FR-4). **Given** any rejected submission, **when** the form shows again, **then** Full name and Email address keep what was typed, both password fields are empty, and no account exists for that email.
- **AC-5** (FR-5). **Given** an account exists for "ana@example.com", **when** someone registers "ANA@example.com", **then** "An account with this email already exists. Please sign in instead." is shown and no new account is created.
- **AC-6** (FR-6). **Given** valid values and an unused email, **when** "Create account" is selected, **then** exactly one account with that name and email exists.
- **AC-7** (FR-7). **Given** a successful registration, **when** the next screen loads, **then** it is the Sign in screen showing "Account created. Please sign in.", and the message is gone after a refresh.
- **AC-8** (FR-8). **Given** Full name "  Ana Silva  " and Email "  ana@example.com  ", **when** registration succeeds, **then** the account is saved as "Ana Silva" with "ana@example.com".
- **AC-9** (FR-9). **Given** a registration with "Ana.Silva@Example.COM", **when** it succeeds, **then** the saved email is "ana.silva@example.com".
- **AC-10** (FR-10). **Given** any registration, successful or not, **when** the user looks at any screen or message, **then** the password never appears, and the saved account does not hold the password in readable form.
- **AC-11** (FR-11). **Given** a successful registration, **when** the Sign in screen loads, **then** the navbar still shows "Get started" and "Sign in".

## 13. Test Cases

| ID | Type | Linked to | Preconditions | Steps | Test data | Expected result |
|---|---|---|---|---|---|---|
| TC-1 | Happy path | FR-6, FR-7, AC-6, AC-7 | Email not registered | Open Create your account, fill all fields, select Create account | Ana Silva / ana@example.com / Secret123 / Secret123 | Sign in screen shows "Account created. Please sign in." One account exists for ana@example.com named "Ana Silva". |
| TC-2 | Happy path | FR-1, FR-2, AC-1, AC-2 | On landing page | Select each of "Get started", "Start tracking free", "Create free account". From Sign in, select "Create one free". On Create your account, select "Sign in". | n/a | The first four each open Create your account, showing 4 labelled fields, the "Create account" button and the "Already have an account? Sign in" line. "Sign in" opens the Sign in screen. |
| TC-3 | Validation | VR-1, FR-3 | n/a | Submit with name invalid, then valid (other fields valid) | "" ; "Ana" | "" shows "Please enter your full name." "Ana" is accepted and goes to the Sign in success screen. |
| TC-4 | Validation | VR-2 | n/a | Submit long name, then valid name | 101 × "a" ; "Ana" | 101 characters shows "Name must be 100 characters or fewer." "Ana" is accepted. |
| TC-5 | Validation | VR-3 | n/a | Submit email blank, then valid | "" ; "ana@example.com" | Blank shows "Please enter your email address." The valid email is accepted. |
| TC-6 | Validation | VR-4 | n/a | Submit invalid email, then valid | "ana.example.com" ; "ana@example.com" | Invalid shows "Please enter a valid email address." The valid email is accepted. |
| TC-7 | Validation | VR-5 | n/a | Submit long email, then valid | 255-character email (`a`×243 + "@example.com") ; "ana@example.com" | 255 characters shows "Email must be 254 characters or fewer." The valid email is accepted. |
| TC-8 | Validation | VR-6 | n/a | Submit password blank, then valid | "" ; "Secret123" | Blank shows "Please enter a password." "Secret123" is accepted. |
| TC-9 | Validation | VR-7 | n/a | Submit short password, then valid | "Sec123" ; "Secret123" | "Sec123" shows "Password must be at least 8 characters." "Secret123" is accepted. |
| TC-10 | Validation | VR-8 | n/a | Submit long password, then valid | 129 × "x" ; "Secret123" | 129 characters shows "Password must be 128 characters or fewer." "Secret123" is accepted. |
| TC-11 | Validation | VR-9 | n/a | Valid password, Confirm blank, then filled | Confirm "" ; "Secret123" | Blank shows "Please confirm your password." Matching confirm is accepted. |
| TC-12 | Validation | VR-10 | n/a | Mismatched confirm, then matching | "Secret124" ; "Secret123" | Mismatch shows "Passwords do not match." Matching confirm is accepted. |
| TC-13 | Boundary | VR-1, VR-2 | n/a | Submit names of each length (other fields valid, a new email each time) | 1 char "A"; 99; 100; 101 characters | 1, 99 and 100 are accepted. 101 shows "Name must be 100 characters or fewer." |
| TC-14 | Boundary | VR-5 | n/a | Submit emails of each length | 253; 254; 255 characters (padding before "@example.com") | 253 and 254 are accepted. 255 shows "Email must be 254 characters or fewer." |
| TC-15 | Boundary | VR-7 | n/a | Submit passwords (confirm matches) | 7; 8; 9 characters | 7 shows "Password must be at least 8 characters." 8 and 9 are accepted. |
| TC-16 | Boundary | VR-8 | n/a | Submit passwords (confirm matches) | 127; 128; 129 characters | 127 and 128 are accepted. 129 shows "Password must be 128 characters or fewer." |
| TC-17 | Error | ER-1, FR-4, AC-4 | n/a | Submit with a short password | Ana Silva / ana@example.com / short / short | "Password must be at least 8 characters." Name and email are kept, both password fields are empty, and no account exists. |
| TC-18 | Error | ER-2, FR-5, AC-5 | ana@example.com registered | Register "ANA@example.com" | Ben / ANA@example.com / Secret123 ×2 | "An account with this email already exists. Please sign in instead." There is still only one account for ana@example.com. |
| TC-19 | Error | ER-3 | Browser offline | Select Create account | Valid data | The browser shows its offline page and no account exists. After reconnecting and resubmitting, the Sign in success screen shows. |
| TC-20 | Error | ER-4 | Spendly made temporarily unable to save | Submit valid form | Valid data | "We couldn't create your account right now. Please try again in a moment." Name and email are kept and no account exists. Submitting again after recovery succeeds. |
| TC-21 | Error | ER-5 | An unexpected failure is forced during account creation | Submit valid form | Valid data | The same message as TC-20, and no partial account exists for that email. |
| TC-22 | Empty / missing | FR-3, VR-1 | n/a | Submit with all four fields blank | All blank | Only "Please enter your full name." is shown. |
| TC-23 | Empty / missing | FR-3, FR-4, AC-3 | n/a | Fill only Full name and Password, submit | "Ana" / "" / "x" / "" | "Please enter your email address." Name "Ana" is kept and the password fields are empty. |
| TC-24 | Empty / missing | EC-15 | Modified page that omits Confirm password | Submit | Other fields valid | "Please confirm your password." No account is created. |
| TC-25 | Empty / missing | FR-6, BR-5 | Only the demo account exists | Register a new user | Ana Silva / ana@example.com / Secret123 ×2 | Success screen. The new account has no expenses. |
| TC-26 | Edge case | EC-1, FR-8, AC-8 | n/a | Submit with surrounding spaces; then a spaces-only name | "  Ana Silva  " / "  ana@example.com  " ; "   " | Saved as "Ana Silva" / "ana@example.com". The spaces-only name shows "Please enter your full name." |
| TC-27 | Edge case | EC-2 | n/a | Register | "José O'Brien-Núñez 😀" | Accepted. The name is saved exactly as typed. |
| TC-28 | Edge case | EC-3, FR-9, AC-9 | Demo account exists | Register "Demo@Spendly.DEV". Separately register "Ana.Silva@Example.COM". | As listed | The first shows ER-2. The second succeeds and is saved as "ana.silva@example.com". |
| TC-29 | Edge case | EC-4 | n/a | Register | ana.silva+spend@mail.example.co.uk | Accepted. |
| TC-30 | Edge case | EC-5 | n/a | Register with password and confirm both " my pass 😀 " | as listed | Accepted. Entering "my pass 😀" (no spaces) in confirm instead shows "Passwords do not match." |
| TC-31 | Edge case | EC-6 | n/a | Password "Secret123", confirm "secret123" | as listed | "Passwords do not match." |
| TC-32 | Edge case | EC-7 | Email not registered | Double-click Create account | Valid data | Exactly one account exists. The user ends on the Sign in success screen or sees ER-2. |
| TC-33 | Edge case | EC-8 | Error message showing | Refresh the page and resend if the browser asks | Short password | The error shows again and no account exists. |
| TC-34 | Edge case | EC-9 | Just registered, on Sign in screen | Refresh | n/a | The Sign in screen shows without "Account created. Please sign in." and there is still one account. |
| TC-35 | Edge case | EC-10 | Just registered ana@example.com | Press Back, re-enter passwords, submit | Same data | ER-2 message. |
| TC-36 | Edge case | EC-11 | Two browsers on Create your account | Submit the same new email in both at the same moment | ana@example.com | One shows the success screen, the other shows ER-2, and one account exists. |
| TC-37 | Edge case | EC-12 | n/a | Paste 10,000 characters into Full name, submit | 10,000 × "a" | "Name must be 100 characters or fewer." The page responds normally. |
| TC-38 | Edge case | EC-13 | n/a | Submit each malformed email | ana@ ; @example.com ; ana@example ; ana silva@example.com ; ana@@example.com | Each shows "Please enter a valid email address." |
| TC-39 | Edge case | EC-14 | n/a | Register with names "<b>Ana</b>" and "' OR 1=1 --" (separate emails) | as listed | Both are accepted and saved exactly as typed. Wherever the names are shown, they appear as literal text with no formatting, and no other accounts are affected. |
| TC-40 | Edge case | EC-16, BR-7 | Demo account exists | Register demo@spendly.dev | Any name / Secret123 ×2 | ER-2. The demo account's name and password are unchanged. |
| TC-41 | Edge case | EC-17 | n/a | Password equals email | ana@example.com as password | Accepted. |
| TC-42 | Permission | Visitor role, FR-6 | Visitor with unused email | Register | ben@example.com | Success screen. The account is created. |
| TC-43 | Permission | Registered user role, FR-5 | ana@example.com registered | Try registering ana@example.com again | as listed | ER-2. Not allowed. |
| TC-44 | Permission | FR-11, AC-11, BR-6 | n/a | Register successfully, look at navbar | Valid data | The navbar still shows "Get started" and "Sign in", so the user is not signed in. |
| TC-45 | Permission | FR-10, AC-10, BR-2 | n/a | Register with an error, then register successfully; check every screen and the saved account | Password "Secret123" | "Secret123" never appears on screen or in messages, and the saved account does not contain "Secret123" in readable form. |
| TC-46 | Regression | Step 01 | n/a | Open the landing, Sign in, Terms and Privacy pages | n/a | Each page loads with its existing content and links. |
| TC-47 | Regression | Step 01 (AC 2, 3), BR-7 | Demo data present | Register a new user, restart the app, then check the demo data | n/a | There is still exactly 1 demo user and 8 demo expenses, unchanged, and the new user still exists. |
| TC-48 | Regression | Step 01 | n/a | Open the Logout, Profile and Add expense links | n/a | They still show their "coming in Step N" placeholder text. |

## 14. Out of Scope

- Signing in with the new account, and the meaning of the Sign in screen's form (a later step).
- Signing out (Step 3), the profile page (Step 4), and recording, editing or deleting expenses (Steps 7 to 9).
- Email verification, welcome emails, password reset and "remember me".
- Signing up with outside accounts (Google, Apple, etc.).
- Changing or deleting an account.
- Password strength meters, character-type rules, and blocking common passwords.
- Limiting how many registration attempts can be made.
- What a signed-in user sees on the Create your account screen (decided when sign-in exists).

## 15. Assumptions and Open Questions

**Decisions from the developer**
- After registering, the user goes to the Sign in screen with "Account created. Please sign in." They are not signed in automatically.
- Passwords must be 8 to 128 characters, with no character-type rules.
- A "Confirm password" field is added.
- Emails are matched ignoring letter case.

**Assumptions (defaults chosen)**
- Full name may be 1 to 100 characters and email up to 254 characters.
- Only one error message is shown at a time, in field order.
- Name and email are kept after an error. Passwords are always cleared.
- Spaces at the start and end are removed from name and email, but not from passwords.
- The duplicate-email message openly says that the email has an account. This is acceptable for this product.
- There is no "I agree to the Terms" checkbox. The Terms and Privacy pages stay reachable from the footer.

**Open questions**
- **OQ-1.** Should the duplicate-email message avoid confirming that an email is registered, for privacy? This currently follows the assumption above.
- **OQ-2.** Should registration require agreeing to the Terms & Conditions and Privacy Policy?
- **OQ-3.** When sign-in exists, what should a signed-in user see if they open the Create your account screen?
- **OQ-4.** Step 01 makes emails unique exactly as typed. This step adds the rule that emails match ignoring letter case, by saving them in lowercase. The demo email is already lowercase, so nothing conflicts today. Any future way of creating accounts must follow the same rule.
