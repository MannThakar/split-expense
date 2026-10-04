---
description: Create a complete spec.md for a step, given a step number and step name
allowed-tools: Read, Glob, Grep, Write, Edit
---

## Context

You are a Senior Product Manager and UX/Product Designer. Your job is to create one complete, well-structured `spec.md` for a single step of the product. The spec is the source of truth for technical planning, implementation and testing, which happen later and separately.

The developer runs this command with two arguments:

1. Step number: `$1`
2. Step name: everything after the step number in `$ARGUMENTS` (it can be several words)

Example: `/<command> 3 user login` creates `specs/03-user-login/spec.md`.

The spec describes WHAT the step does and WHY, how it behaves, and how to prove it works. It does not describe HOW it is built: no databases, tables, APIs, frameworks, libraries, code or file structures.

Before writing, read for product context:

1. All existing specs (Glob `specs/**/spec.md`, then Read each one), so this step builds on earlier steps and does not contradict them.
2. `README.md` and `CLAUDE.md` at the repo root, if they exist.
3. Any screenshots, images, links or notes the developer shared in the conversation.

## Instructions

1. Validate the arguments.
   - `$1` must be a positive whole number. Pad it to two digits (`3` becomes `03`).
   - The step name must not be empty. Convert it to a slug: lowercase, spaces and underscores become `-`, other special characters removed.
   - The output path is `specs/<step>-<step-slug>/spec.md`.

2. Understand the step. Write a one or two sentence summary of what this step delivers and who it is for.

3. Find the gaps. List what is unclear about behavior, rules or user experience. Ask the developer at most 5 short questions, each answerable in one word or one line, with your recommended answer marked. Never ask technical questions. Wait for the answers. Any question left unanswered uses your recommended default and is recorded as an assumption.

4. Write the spec with exactly these numbered sections, in this order. Do not skip a section; if one does not apply, write "Not applicable" and say why.
   1. **Title block**: `# Step <step>: <Step Name>`, then Status (Draft), Last updated (today's date), and Depends on (earlier steps this one needs, or "None").
   2. **Overview**: the problem, who has it, and why this step matters.
   3. **Goals and Non-Goals**: what success looks like, and what this step deliberately does not do.
   4. **Users and Roles**: each type of user and what they are allowed to do in this step.
   5. **User Scenarios**: the main situations, written as short user stories ("As a ..., I want ..., so that ...").
   6. **Functional Requirements**: numbered FR-1, FR-2, ... Each one is a single, testable statement such as "The user can ..." or "The product shows ...".
   7. **User Flow and Screens**: the step-by-step flow from entry to outcome, what each screen shows, and the exact wording of key labels, buttons and messages.
   8. **Validation Rules**: a table with one row per input or field: field, required or optional, allowed values or format, minimum and maximum, and the exact message shown when it is invalid. Number each rule VR-1, VR-2, ...
   9. **States**: what the user sees in the empty, loading, success, error, partial, disabled and first-time states.
   10. **Error Handling**: each failure the user can hit (invalid input, lost connection, timeout, action not allowed, something not found, duplicate, unexpected failure), the message shown, and how the user recovers. Number each one ER-1, ER-2, ...
   11. **Edge Cases**: unusual but possible situations, numbered EC-1, EC-2, ..., each with the expected behavior. Always consider: boundary values, very long or very short input, special characters and emoji, duplicate submissions, double clicks, going back or refreshing mid-flow, two people changing the same thing, missing or partial data, and very large amounts of data.
   12. **Business Rules and Constraints**: rules the product must always follow (limits, ordering, who can see what, what can never be deleted).
   13. **Acceptance Criteria**: numbered AC-1, AC-2, ..., written as Given / When / Then. Every FR has at least one AC.
   14. **Test Cases**: a table with columns ID, Type, Linked to (FR, VR, ER, EC or AC numbers), Preconditions, Steps, Test data, Expected result. Number them TC-1, TC-2, ... Include every type below:
       - Happy path: the main flow works end to end.
       - Validation: one test per validation rule, with both a valid and an invalid value.
       - Boundary: exactly at, just below and just above every minimum and maximum.
       - Error: one test per error in Error Handling.
       - Empty and missing data: no data yet, blank fields, partial data.
       - Edge case: one test per edge case.
       - Permission: each role tries an action it is and is not allowed to do.
       - Regression: earlier steps that this step touches still work.
   15. **Out of Scope**: what is left for later steps.
   16. **Assumptions and Open Questions**: defaults you chose, and questions still waiting on the product owner.

5. Review the spec before saving and fix anything that fails:
   - Every FR has at least one AC and at least one test case.
   - Every validation rule, error and edge case has at least one test case.
   - Every state and error says exactly what the user sees.
   - Every test case has a concrete expected result, not "works correctly".
   - No technical implementation detail appears (scan for words like database, table, API, endpoint, framework, library, component, JSON, schema, and rewrite them as user-facing behavior).
   - Nothing contradicts an earlier step's spec.

6. Save the file with Write to `specs/<step>-<step-slug>/spec.md`.

## Edge Cases

- **Missing arguments**: if the step number or step name is missing, stop, show the usage (`/<command> <step-number> <step-name>`, for example `/<command> 3 user login`) and create no file.
- **Step number is not a positive whole number** (for example `abc`, `0` or `-2`): stop, explain the rule, show the usage and create no file.
- **Arguments look swapped** (for example `login 3`): point it out and ask the developer to confirm before continuing.
- **Spec already exists at the path**: do not overwrite it. Read it, tell the developer, and ask whether to update it or stop. When updating, keep what is still correct, change only what the new information affects, keep existing IDs (FR, VR, ER, EC, AC, TC) stable, and update the date.
- **Same step name exists under a different number**: name the existing folder and ask whether this is a new step or the same one.
- **Step number already used by a different step**: warn the developer and ask whether to continue with this number.
- **No `specs/` folder yet**: this is the first spec. Create the folder along with the file.
- **Very little detail given** (only a step name): do not invent a large product. Ask the clarifying questions, write a lean but complete spec with every section present, and list the gaps as open questions.
- **Developer asks a technical question or for implementation**: explain that this command only writes the spec and that technical planning comes next. Record any real product constraint behind the question as a business rule.
- **A reference cannot be read** (missing image, broken link): say which one, continue without it, and list it under open questions.
- **Conflict with an earlier step's spec**: do not change the earlier spec. Describe the conflict and list it under open questions.
- **The write fails**: report the error and the intended path, and do not claim the spec was created.

## Expected Output

After saving, report back with:

- `Spec created: .claude/specs/<step>_<step-slug>.md` (or `Spec updated: ...`)
- Summary: one or two sentences on what the step delivers and why.
- Coverage counts: functional requirements, validation rules, errors, edge cases, acceptance criteria and test cases (with the count of each test type).
- Coverage check: confirm every FR, VR, ER and EC is linked to at least one test case, or list the ones that are not.
- Assumptions made: a short list, or "none".
- Open questions: a short list, or "none".
- Next step: review the spec, then start technical planning (for example in plan mode).

Do not print the whole spec in the reply; it is in the file.
