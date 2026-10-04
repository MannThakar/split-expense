---
description: Create a new Git branch from the latest main branch
argument-hint: "<branch-name>"
allowed-tools: Bash(git:*)
---

## Usage

Run this command from the Git repository:

/create-branch <branch-name>

Examples:

/create-branch feat/user-authentication
/create-branch fix/login-validation
/create-branch chore/update-dependencies

## What This Command Does

The purpose of this command is to create a new branch from the latest
remote `main` branch.

Follow the steps below in the exact order.

### 1. Verify Git Repository

- Verify that the current directory is a Git repository.
- If it is not a Git repository, stop and report the issue.

### 2. Validate Branch Name Argument

Read the branch name from `$ARGUMENTS`.

The branch name is required.

If no branch name is provided:

- Stop immediately.
- Ask the user to provide a branch name.

The branch name must start with an approved Git workflow prefix.

At minimum, allow:

- `feat/` — new feature
- `fix/` — bug fix
- `chore/` — maintenance or configuration
- `refactor/` — code refactoring
- `docs/` — documentation changes
- `test/` — tests
- `perf/` — performance improvements
- `build/` — build-related changes
- `ci/` — CI/CD changes

Examples of valid branch names:

```text
feat/user-authentication
fix/login-validation
chore/update-dependencies
refactor/api-service
docs/setup-guide
test/user-service
perf/dashboard-rendering
build/update-vite
ci/github-actions
```
