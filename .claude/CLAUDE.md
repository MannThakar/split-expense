# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

"Spendly" — a Flask expense tracker built as a **teaching scaffold**. The UI shell (landing, auth pages, legal pages, full CSS design system) is finished; the application logic is deliberately unimplemented and is filled in step by step. `app.py` marks the remaining work with placeholder routes that return strings like `"Add expense — coming in Step 7"`, and `database/db.py` is a comment block specifying the three functions to write. Preserve that step-by-step structure: implement the step being asked for, don't jump ahead and build out unrelated placeholder routes.

## Commands

Windows venv (`venv/Scripts/`), Python on the path as `python`:

```bash
venv/Scripts/python app.py          # dev server: http://localhost:5001, debug=True
venv/Scripts/pip install -r requirements.txt
venv/Scripts/python -m pytest       # no tests exist yet; pytest + pytest-flask are installed
venv/Scripts/python -m pytest tests/test_auth.py::test_register_creates_user   # single test
```

There is no build step, no linter, and no JS toolchain — CSS and JS are hand-written static files served directly by Flask.

## Architecture

- **`app.py`** — the entire application: a module-level `app = Flask(__name__)` plus route functions. No blueprints, no app factory, no config module. New routes go here.
- **`database/db.py`** — the only data layer. Raw `sqlite3` (no ORM) against `expense_tracker.db` (gitignored, created at runtime). The intended API is `get_db()` (connection with `row_factory` set and foreign keys enabled), `init_db()` (`CREATE TABLE IF NOT EXISTS`), and `seed_db()` (sample dev data).
- **`templates/`** — Jinja2. Every page does `{% extends "base.html" %}` and fills `{% block title %}` and `{% block content %}`; `base.html` also offers `head` and `scripts` blocks and owns the navbar and footer. Links use `url_for('<route_function>')`, so renaming a route function breaks templates.
- **`static/css/style.css`** — one ~725-line stylesheet, no framework. Design tokens live in `:root` (`--ink*`, `--paper*`, `--accent*`, `--radius-*`, `--font-display`/`--font-body`); use them rather than literal colors. Sections are separated by full-width `/* ---- */` banner comments matching the page or component (Navbar, Hero, Buttons, Auth pages, Legal pages, Footer, Responsive) — add new component styles as a new banner-comment section, and keep `Responsive` last.
- **`static/js/main.js`** — currently empty; the app is server-rendered, so reach for JS only when a feature genuinely needs it.

## Conventions

- Forms POST to a literal path (`action="/register"`) and render errors via an `{% if error %}` block, so auth routes need `methods=["GET", "POST"]` and re-render their own template with `error=...` rather than redirecting.
- `werkzeug` is pinned in requirements specifically for `generate_password_hash` / `check_password_hash` — hash passwords with it, never store plaintext.
- The app runs on **port 5001** (not 5000).
