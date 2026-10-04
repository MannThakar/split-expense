import os

import psycopg2
import pytest

# Point the app at a separate test database before app.py is imported,
# since importing it runs init_db() and seed_db().
TEST_DB_NAME = os.environ.setdefault("DB_NAME", "expense_tracker_test")

from database import db  # noqa: E402


def _ensure_test_database():
    """Creates the test database if missing, via the 'postgres' maintenance DB."""
    os.environ["DB_NAME"] = "postgres"
    try:
        conn = db.get_db()
    finally:
        os.environ["DB_NAME"] = TEST_DB_NAME
    conn.autocommit = True
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (TEST_DB_NAME,))
            if not cur.fetchone():
                # Identifier comes from our own constant/env, not user input.
                cur.execute(f'CREATE DATABASE "{TEST_DB_NAME}"')
    finally:
        conn.close()


_ensure_test_database()

import app as app_module  # noqa: E402


@pytest.fixture
def app():
    app_module.app.config.update(TESTING=True)
    return app_module.app


@pytest.fixture(autouse=True)
def clean_db():
    """Every test starts with only the demo user and its 8 expenses."""
    conn = db.get_db()
    try:
        with conn.cursor() as cur:
            cur.execute("TRUNCATE expenses, users RESTART IDENTITY CASCADE")
        conn.commit()
    finally:
        conn.close()
    db.seed_db()
    yield


def query(sql, params=()):
    conn = db.get_db()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            return cur.fetchall()
    finally:
        conn.close()


def count_users(email):
    return query("SELECT count(*) AS n FROM users WHERE LOWER(email) = LOWER(%s)", (email,))[0]["n"]


def get_user(email):
    rows = query("SELECT * FROM users WHERE email = %s", (email,))
    return rows[0] if rows else None


VALID = {
    "name": "Ana Silva",
    "email": "ana@example.com",
    "password": "Secret123",
    "confirm_password": "Secret123",
}


def post_register(client, follow_redirects=False, omit=(), **overrides):
    data = {**VALID, **overrides}
    if "password" in overrides and "confirm_password" not in overrides:
        data["confirm_password"] = overrides["password"]
    for field in omit:
        data.pop(field, None)
    return client.post("/register", data=data, follow_redirects=follow_redirects)
