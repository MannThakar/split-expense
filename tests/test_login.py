"""Tests for Step 03: Login User (.claude/specs/03_login-user.md).

TC numbers refer to the spec's test case table. Browser-only cases
(TC-15 offline, TC-24 double click, TC-25 resend, TC-27 back button,
TC-35 browser restart) are verified manually.
"""
import re

import psycopg2
import pytest
from markupsafe import escape

import app as app_module
from conftest import get_user, post_register, query
from database.db import DEMO_EMAIL, DEMO_PASSWORD, create_user

INCORRECT = "Incorrect email or password."
UNAVAILABLE = "We couldn't sign you in right now. Please try again in a moment."
SIGNED_OUT = "You have been signed out."
ACCOUNT_CREATED = "Account created. Please sign in."


def body(response):
    return response.get_data(as_text=True)


def shows(response, message):
    return str(escape(message)) in body(response)


def post_login(client, email=DEMO_EMAIL, password=DEMO_PASSWORD, omit=(), follow_redirects=False):
    data = {"email": email, "password": password}
    for field in omit:
        data.pop(field)
    return client.post("/login", data=data, follow_redirects=follow_redirects)


def signed_in_as(client):
    with client.session_transaction() as sess:
        return sess.get("user_id")


def demo_id():
    return get_user(DEMO_EMAIL)["id"]


def assert_signed_in(response, client, user_id=None):
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/profile")
    assert signed_in_as(client) == (user_id or demo_id())


def assert_rejected(response, client, message, email=None):
    assert response.status_code == 200
    assert shows(response, message)
    assert signed_in_as(client) is None
    html = body(response)
    if email is not None:
        assert f'value="{escape(email)}"' in html
    # Password field is never pre-filled (FR-7, FR-12).
    password_input = re.search(r'<input[^>]*name="password"[^>]*>', html).group(0)
    assert "value=" not in password_input


def navbar(html):
    """Only the top navbar; the landing hero has its own Sign in button."""
    return re.search(r'<nav class="navbar">.*?</nav>', html, re.S).group(0)


def assert_signed_out_nav(html):
    html = navbar(html)
    assert "Get started" in html
    assert 'href="/login"' in html
    assert "Sign out" not in html


def assert_signed_in_nav(html):
    html = navbar(html)
    assert "Sign out" in html
    assert "Get started" not in html
    assert 'href="/login"' not in html


def email_of_length(n):
    domain = "@example.com"
    return "a" * (n - len(domain)) + domain


# --------------------------------------------------------------------- #
# Happy path                                                             #
# --------------------------------------------------------------------- #

def test_tc1_sign_in_opens_profile_and_navbar_shows_sign_out(client):
    assert_signed_in(post_login(client), client)
    assert_signed_in_nav(body(client.get("/")))


def test_tc2_sign_in_page_contents_and_links(client):
    html = body(client.get("/login"))
    for text in ("Welcome back", "Sign in to your Spendly account", "Email address",
                 "Password", "Sign in", "Don't have an account?", "Create one free"):
        assert text in html
    assert 'href="/register"' in html
    assert 'href="/login"' in body(client.get("/register"))
    assert 'href="/login"' in body(client.get("/"))


def test_tc3_sign_out_shows_message_once(client):
    post_login(client)
    response = client.get("/logout", follow_redirects=True)
    assert response.request.path == "/login"
    assert shows(response, SIGNED_OUT)
    assert 'class="auth-success"' in body(response)
    assert_signed_out_nav(body(response))
    assert signed_in_as(client) is None
    assert not shows(client.get("/login"), SIGNED_OUT)


@pytest.mark.parametrize("path", ["/", "/terms", "/privacy"])
def test_tc4_stays_signed_in_across_pages(client, path):
    post_login(client)
    assert_signed_in_nav(body(client.get(path)))


# --------------------------------------------------------------------- #
# Validation                                                             #
# --------------------------------------------------------------------- #

@pytest.mark.parametrize(
    "email, password, message",
    [
        ("", DEMO_PASSWORD, "Please enter your email address."),              # TC-5
        ("   ", DEMO_PASSWORD, "Please enter your email address."),
        ("demo.spendly.dev", DEMO_PASSWORD, "Please enter a valid email address."),  # TC-6
        (email_of_length(255), DEMO_PASSWORD, "Email must be 254 characters or fewer."),  # TC-7
        (DEMO_EMAIL, "", "Please enter your password."),                      # TC-8
    ],
)
def test_tc5_to_tc8_invalid_then_valid(client, email, password, message):
    assert_rejected(post_login(client, email=email, password=password), client, message)
    assert_signed_in(post_login(client), client)


def test_tc9_only_first_error_shown(client):
    response = post_login(client, email="", password="")
    assert shows(response, "Please enter your email address.")
    assert not shows(response, "Please enter your password.")

    response = post_login(client, email="abc", password="")
    assert shows(response, "Please enter a valid email address.")
    assert not shows(response, "Please enter your password.")


@pytest.mark.parametrize(
    "email, message",
    [
        ("a", "Please enter a valid email address."),
        (email_of_length(253), INCORRECT),
        (email_of_length(254), INCORRECT),
        (email_of_length(255), "Email must be 254 characters or fewer."),
    ],
)
def test_tc10_email_length_boundaries(client, email, message):
    assert_rejected(post_login(client, email=email, password="Secret123"), client, message)


def test_tc11_password_length_boundaries(client):
    create_user("Long", "long@example.com", "x" * 128)
    assert_rejected(post_login(client, email="long@example.com", password=""),
                    client, "Please enter your password.")
    for n in (1, 127, 129):
        assert_rejected(post_login(client, email="long@example.com", password="x" * n),
                        client, INCORRECT)
    user_id = get_user("long@example.com")["id"]
    assert_signed_in(post_login(client, email="long@example.com", password="x" * 128),
                     client, user_id)


# --------------------------------------------------------------------- #
# Errors                                                                 #
# --------------------------------------------------------------------- #

def test_tc12_invalid_email_kept(client):
    response = post_login(client, email="demo@spendly", password=DEMO_PASSWORD)
    assert_rejected(response, client, "Please enter a valid email address.", email="demo@spendly")
    assert DEMO_PASSWORD not in body(response)


def test_tc13_tc14_wrong_password_and_unknown_email_look_identical(client):
    wrong = post_login(client, email=DEMO_EMAIL, password="wrongpass1")
    unknown = post_login(client, email="nobody@example.com", password="wrongpass1")
    assert_rejected(wrong, client, INCORRECT, email=DEMO_EMAIL)
    assert_rejected(unknown, client, INCORRECT, email="nobody@example.com")
    assert "wrongpass1" not in body(wrong)
    assert body(wrong).replace(DEMO_EMAIL, "X") == body(unknown).replace("nobody@example.com", "X")


@pytest.mark.parametrize(
    "exc",
    [psycopg2.OperationalError("server unavailable"),  # TC-16 (ER-4)
     RuntimeError("boom")],                            # TC-17 (ER-5)
)
def test_tc16_tc17_lookup_failure_shows_retry_message(client, monkeypatch, exc):
    def failing_lookup(*args, **kwargs):
        raise exc

    monkeypatch.setattr(app_module, "get_user_by_email", failing_lookup)
    response = post_login(client)
    assert_rejected(response, client, UNAVAILABLE, email=DEMO_EMAIL)
    assert_signed_out_nav(body(response))

    monkeypatch.undo()
    assert_signed_in(post_login(client), client)


# --------------------------------------------------------------------- #
# Empty / missing                                                        #
# --------------------------------------------------------------------- #

def test_tc18_first_visit_is_empty(client):
    html = body(client.get("/login"))
    assert 'placeholder="nitish@example.com"' in html
    assert 'placeholder="Your password"' in html
    assert 'value=""' in html
    assert "auth-error" not in html and "auth-success" not in html


def test_tc19_only_email_filled(client):
    assert_rejected(post_login(client, password=""), client,
                    "Please enter your password.", email=DEMO_EMAIL)


@pytest.mark.parametrize("field, message", [
    ("password", "Please enter your password."),     # TC-20
    ("email", "Please enter your email address."),  # EC-12
])
def test_tc20_missing_field_treated_as_blank(client, field, message):
    assert_rejected(post_login(client, omit=(field,)), client, message)


# --------------------------------------------------------------------- #
# Edge cases                                                             #
# --------------------------------------------------------------------- #

def test_tc21_email_case_and_spaces_ignored(client):
    assert_signed_in(post_login(client, email="  Demo@Spendly.DEV  "), client)


@pytest.mark.parametrize("password", ["DEMO1234", "demo1234 ", " demo1234"])  # TC-22, TC-23
def test_tc22_tc23_password_exact_match(client, password):
    assert_rejected(post_login(client, password=password), client, INCORRECT)


def test_tc26_signed_in_user_cannot_switch_account(client):
    create_user("Ana Silva", "ana@example.com", "Secret123")
    post_login(client)
    response = post_login(client, email="ana@example.com", password="Secret123")
    assert response.headers["Location"].endswith("/profile")
    assert signed_in_as(client) == demo_id()


def test_tc28_sign_out_in_one_browser_keeps_other_signed_in(app):
    a, b = app.test_client(), app.test_client()
    post_login(a)
    post_login(b)
    a.get("/logout")
    assert signed_in_as(a) is None
    assert signed_in_as(b) == demo_id()
    assert_signed_in_nav(body(b.get("/")))


def test_tc29_very_long_input(client):
    assert_rejected(post_login(client, email="a" * 10_000), client,
                    "Email must be 254 characters or fewer.")
    assert_rejected(post_login(client, password="a" * 10_000), client, INCORRECT)


def test_tc30_code_like_input(client):
    response = post_login(client, email="' OR 1=1 --")
    assert_rejected(response, client, "Please enter a valid email address.")
    assert str(escape("' OR 1=1 --")) in body(response)
    assert_rejected(post_login(client, password="' OR 1=1 --"), client, INCORRECT)


def test_tc31_password_with_emoji_and_spaces(client):
    create_user("Ben", "ben@example.com", " my pass 😀 ")
    user_id = get_user("ben@example.com")["id"]
    assert_signed_in(post_login(client, email="ben@example.com", password=" my pass 😀 "),
                     client, user_id)


def test_tc32_sign_out_while_signed_out(client):
    response = client.get("/logout", follow_redirects=True)
    assert response.request.path == "/login"
    assert not shows(response, SIGNED_OUT)
    assert "auth-error" not in body(response)


def test_tc33_many_wrong_attempts_then_correct(client):
    for _ in range(10):
        assert_rejected(post_login(client, password="wrongpass1"), client, INCORRECT)
    assert_signed_in(post_login(client), client)


def test_tc34_register_then_sign_in_then_sign_out(client):
    response = post_register(client, name="Cara", email="cara@example.com", follow_redirects=True)
    assert shows(response, ACCOUNT_CREATED)
    user_id = get_user("cara@example.com")["id"]
    assert_signed_in(post_login(client, email="cara@example.com", password="Secret123"),
                     client, user_id)
    response = client.get("/logout", follow_redirects=True)
    assert shows(response, SIGNED_OUT)
    assert not shows(response, ACCOUNT_CREATED)


# --------------------------------------------------------------------- #
# Permissions                                                            #
# --------------------------------------------------------------------- #

@pytest.mark.parametrize("path", ["/login", "/register"])
def test_tc36_visitor_sees_forms(client, path):
    response = client.get(path)
    assert response.status_code == 200
    assert "<form" in body(response)


@pytest.mark.parametrize("path", ["/login", "/register"])  # TC-37, TC-38
def test_tc37_tc38_signed_in_user_redirected_to_profile(client, path):
    post_login(client)
    response = client.get(path)
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/profile")
    assert signed_in_as(client) == demo_id()


def test_tc38_signed_in_user_cannot_register(client):
    post_login(client)
    post_register(client, email="sneaky@example.com")
    assert get_user("sneaky@example.com") is None


# --------------------------------------------------------------------- #
# Regression                                                             #
# --------------------------------------------------------------------- #

def test_tc39_register_then_sign_in_with_different_case(client):
    post_register(client, name="Dev", email="Dev.User@Example.COM")
    user_id = get_user("dev.user@example.com")["id"]
    assert_signed_in(post_login(client, email="dev.user@example.com", password="Secret123"),
                     client, user_id)


def test_tc40_registering_does_not_sign_in(client):
    response = post_register(client, email=DEMO_EMAIL)
    assert shows(response, "An account with this email already exists. Please sign in instead.")
    response = post_register(client, email="eve@example.com", follow_redirects=True)
    assert shows(response, ACCOUNT_CREATED)
    assert signed_in_as(client) is None
    assert_signed_out_nav(body(response))


def test_tc41_demo_data_unchanged_after_sign_ins(client):
    for _ in range(3):
        post_login(client)
        client.get("/logout")
    demo = get_user(DEMO_EMAIL)
    assert demo["name"] == "Demo User"
    rows = query("SELECT count(*) AS n FROM expenses WHERE user_id = %s", (demo["id"],))
    assert rows[0]["n"] == 8


@pytest.mark.parametrize("path", ["/terms", "/privacy"])
def test_tc42_legal_pages_in_both_states(client, path):
    response = client.get(path)
    assert response.status_code == 200
    assert_signed_out_nav(body(response))
    post_login(client)
    response = client.get(path)
    assert response.status_code == 200
    assert_signed_in_nav(body(response))
    assert 'href="/terms"' in body(response) and 'href="/privacy"' in body(response)
