---
description: Commit all staged changes with a proper conventional commit message, push the current branch, and then checkout main
allowed-tools: Bash(git:*)
---

## Usage

Run this command from the Git repository:

/push-code

The command does not require any arguments.

## What This Command Does

Follow these steps in order.

### 1. Check the Git Repository

- Verify that the current directory is a Git repository.
- If it is not a Git repository, stop and report the issue.
- Get the current branch name.
- Never assume the current branch name.

### 2. Check the Current Branch

- Store the current branch name before making any changes.
- If the current branch is `main`, stop without committing or pushing.
- The purpose of this command is to commit and push the current working branch, then switch to `main`.

### 3. Check Staged Changes

Check the Git staging area.

- Only commit files that are already staged.
- Do not automatically run `git add`.
- Do not stage unstaged or untracked files.
- If there are no staged files, stop and report that there are no staged changes to commit.

Before committing, inspect the staged diff to understand what was changed.

### 4. Determine the Commit Type

Based on the staged changes, determine whether the commit is primarily a:

- `feat` — new functionality or feature
- `fix` — bug fix or correction

Do not use `feat` or `fix` randomly.

Use the staged diff to determine the most appropriate type.

Examples:

```text
feat: add user authentication
feat: add project filtering
fix: resolve login validation error
fix: handle null API response
```
