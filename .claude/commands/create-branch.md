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

Create a new Git branch from the latest `main` branch.

The command must perform all validations before creating the branch.

The user must:

- Be currently on the `main` branch.
- Have a completely clean working tree.
- Have no staged changes.
- Have no unstaged changes.
- Provide a valid branch name.
- Provide a branch name that does not already exist locally or remotely.

Follow the steps below in the exact order.

## 1. Verify Git Repository

Verify that the current directory is a Git repository.

If it is not a Git repository:

- Stop immediately.
- Do not run branch creation commands.
- Report the issue to the user.

## 2. Validate Branch Name Argument

Read the branch name from `$ARGUMENTS`.

A branch name is required.

If no branch name is provided:

- Stop immediately.
- Ask the user to provide a branch name.

The branch name must start with one of these approved prefixes:

- `feat/` — new feature
- `fix/` — bug fix
- `chore/` — maintenance or configuration
- `refactor/` — code refactoring
- `docs/` — documentation
- `test/` — testing
- `perf/` — performance improvements
- `build/` — build-related changes
- `ci/` — CI/CD changes

Valid examples:

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
