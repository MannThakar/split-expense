"""Tests for Step 02: Register User (.claude/specs/02_register-user.md).

TC numbers refer to the spec's test case table. Browser-only cases
(TC-2 link clicks, TC-19 offline, TC-32 double click, TC-33 refresh/resend)
are verified manually.
"""
import psycopg2
import pytest
from markupsafe import escape
from werkzeug.security import check_password_hash

import app as app_module
from conftest import VALID, count_users, get_user, post_register, query
from database.db import DEMO_EMAIL, EmailTakenError, create_user

SUCCESS = "Account created. Please sign in."
DUPLICATE = "An account with this email already exists. Please sign in instead."
UNAVAILABLE = "We couldn't create your account right now. Please try again in a moment."


def body(response):
    return response.get_data(as_text=True)


def shows(response, message):
    return str(escape(message)) in body(response)


def assert_success(response):
    assert response.status_code == 200
    assert response.request.path == "/login"
    assert shows(response, SUCCESS)


def assert_rejected(response, message, email=VALID["email"]):
    assert response.status_code == 200
    assert response.request.path == "/register"
    assert shows(response, message)
    assert count_users(email) == 0


def email_of_length(n):
    domain = "@example.com"
    return "a" * (n - len(domain)) + domain


# --------------------------------------------------------------------- #
# Happy path                                                             #
# --------------------------------------------------------------------- #

def test_tc1_register_creates_user_and_redirects_to_sign_in(client):
    response = post_register(client)
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/login")

    response = client.get("/login")
    assert shows(response, SUCCESS)
    user = get_user("ana@example.com")
    assert user["name"] == "Ana Silva"
    assert count_users("ana@example.com") == 1


def test_tc2_register_page_shows_four_fields_and_links(client):
    html = body(client.get("/register"))
    for label in ("Full name", "Email address", "Password", "Confirm password"):
        assert f">{label}</label>" in html
    for field in ('name="name"', 'name="email"', 'name="password"', 'name="confirm_password"'):
        assert field in html
    assert "Create account" in html
    assert "Already have an account?" in html
    assert 'href="/login"' in html
    # Entry points to the register page (FR-1).
    assert 'href="/register"' in body(client.get("/"))
    assert 'href="/register"' in body(client.get("/login"))


# --------------------------------------------------------------------- #
# Validation (TC-3 .. TC-12): invalid value rejected, valid accepted     #
# --------------------------------------------------------------------- #

@pytest.mark.parametrize(
    "field, invalid, message, valid",
    [
        ("name", "", "Please enter your full name.", "Ana"),                                 # TC-3
        ("name", "a" * 101, "Name must be 100 characters or fewer.", "Ana"),                 # TC-4
        ("email", "", "Please enter your email address.", "ana@example.com"),                # TC-5
        ("email", "ana.example.com", "Please enter a valid email address.", "ana@example.com"),  # TC-6
        ("email", email_of_length(255), "Email must be 254 characters or fewer.", "ana@example.com"),  # TC-7
        ("password", "", "Please enter a password.", "Secret123"),                           # TC-8
        ("password", "Sec123", "Password must be at least 8 characters.", "Secret123"),      # TC-9
        ("password", "x" * 129, "Password must be 128 characters or fewer.", "Secret123"),   # TC-10
        ("confirm_password", "", "Please confirm your password.", "Secret123"),              # TC-11
        ("confirm_password", "Secret124", "Passwords do not match.", "Secret123"),           # TC-12
    ],
)
def test_validation_rules(client, field, invalid, message, valid):
    response = post_register(client, follow_redirects=True, **{field: invalid})
    assert_rejected(response, message)

    response = post_register(client, follow_redirects=True, **{field: valid})
    assert_success(response)


# --------------------------------------------------------------------- #
# Boundaries (TC-13 .. TC-16)                                            #
# --------------------------------------------------------------------- #

@pytest.mark.parametrize("length, ok", [(1, True), (99, True), (100, True), (101, False)])
def test_tc13_name_length_boundaries(client, length, ok):
    response = post_register(client, follow_redirects=True, name="A" * length)
    if ok:
        assert_success(response)
    else:
        assert_rejected(response, "Name must be 100 characters or fewer.")


@pytest.mark.parametrize("length, ok", [(253, True), (254, True), (255, False)])
def test_tc14_email_length_boundaries(client, length, ok):
    email = email_of_length(length)
    response = post_register(client, follow_redirects=True, email=email)
    if ok:
        assert_success(response)
        assert count_users(email) == 1
    else:
        assert_rejected(response, "Email must be 254 characters or fewer.", email=email)


@pytest.mark.parametrize("length, ok", [(7, False), (8, True), (9, True)])
def test_tc15_password_min_boundaries(client, length, ok):
    response = post_register(client, follow_redirects=True, password="p" * length)
    if ok:
        assert_success(response)
    else:
        assert_rejected(response, "Password must be at least 8 characters.")


@pytest.mark.parametrize("length, ok", [(127, True), (128, True), (129, False)])
def test_tc16_password_max_boundaries(client, length, ok):
    response = post_register(client, follow_redirects=True, password="p" * length)
    if ok:
        assert_success(response)
    else:
        assert_rejected(response, "Password must be 128 characters or fewer.")


# --------------------------------------------------------------------- #
# Errors                                                                 #
# --------------------------------------------------------------------- #

def test_tc17_invalid_input_keeps_name_and_email_and_clears_passwords(client):
    response = post_register(client, password="short")
    assert_rejected(response, "Password must be at least 8 characters.")
    html = body(response)
    assert 'value="Ana Silva"' in html
    assert 'value="ana@example.com"' in html
    assert "short" not in html


def test_tc18_duplicate_email_ignoring_case(client):
    create_user("Ana Silva", "ana@example.com", "Secret123")
    response = post_register(client, name="Ben", email="ANA@example.com")
    assert shows(response, DUPLICATE)
    assert count_users("ana@example.com") == 1
    assert get_user("ana@example.com")["name"] == "Ana Silva"


@pytest.mark.parametrize(
    "exc",
    [psycopg2.OperationalError("server unavailable"),  # TC-20 (ER-4)
     RuntimeError("boom")],                            # TC-21 (ER-5)
)
def test_tc20_tc21_save_failure_shows_retry_message(client, monkeypatch, exc):
    def failing_create_user(*args, **kwargs):
        raise exc

    monkeypatch.setattr(app_module, "create_user", failing_create_user)
    response = post_register(client)
    assert_rejected(response, UNAVAILABLE)
    assert 'value="Ana Silva"' in body(response)

    monkeypatch.undo()
    assert_success(post_register(client, follow_redirects=True))


# --------------------------------------------------------------------- #
# Empty and missing data                                                 #
# --------------------------------------------------------------------- #

def test_tc22_all_blank_shows_only_first_error(client):
    response = post_register(client, name="", email="", password="", confirm_password="")
    html = body(response)
    assert shows(response, "Please enter your full name.")
    assert "Please enter your email address." not in html
    assert "Please enter a password." not in html
    assert html.count('class="auth-error"') == 1


def test_tc23_partial_form_shows_first_failing_field(client):
    response = post_register(client, name="Ana", email="", password="x", confirm_password="")
    assert shows(response, "Please enter your email address.")
    assert 'value="Ana"' in body(response)


def test_ac3_name_error_wins_over_password_error(client):
    response = post_register(client, name="", password="short")
    assert shows(response, "Please enter your full name.")
    assert "Password must be at least 8 characters." not in body(response)


def test_tc24_missing_confirm_field_treated_as_blank(client):
    response = post_register(client, omit=("confirm_password",))
    assert_rejected(response, "Please confirm your password.")


def test_tc25_new_account_has_no_expenses(client):
    assert_success(post_register(client, follow_redirects=True))
    user = get_user("ana@example.com")
    rows = query("SELECT count(*) AS n FROM expenses WHERE user_id = %s", (user["id"],))
    assert rows[0]["n"] == 0


# --------------------------------------------------------------------- #
# Edge cases                                                             #
# --------------------------------------------------------------------- #

def test_tc26_surrounding_spaces_trimmed(client):
    response = post_register(client, follow_redirects=True,
                             name="  Ana Silva  ", email="  ana@example.com  ")
    assert_success(response)
    assert get_user("ana@example.com")["name"] == "Ana Silva"

    response = post_register(client, name="   ", email="other@example.com")
    assert_rejected(response, "Please enter your full name.", email="other@example.com")


def test_tc27_special_characters_and_emoji_in_name(client):
    name = "José O'Brien-Núñez 😀"
    assert_success(post_register(client, follow_redirects=True, name=name))
    assert get_user("ana@example.com")["name"] == name


def test_tc28_email_saved_lowercase_and_demo_case_variant_rejected(client):
    response = post_register(client, email="Demo@Spendly.DEV")
    assert shows(response, DUPLICATE)

    assert_success(post_register(client, follow_redirects=True, email="Ana.Silva@Example.COM"))
    assert get_user("ana.silva@example.com") is not None
    assert get_user("Ana.Silva@Example.COM") is None


def test_tc29_plus_and_multipart_domain_email_accepted(client):
    email = "ana.silva+spend@mail.example.co.uk"
    assert_success(post_register(client, follow_redirects=True, email=email))
    assert count_users(email) == 1


def test_tc30_password_with_spaces_and_emoji_kept_as_typed(client):
    password = " my pass 😀 "
    response = post_register(client, password=password, confirm_password="my pass 😀")
    assert_rejected(response, "Passwords do not match.")

    assert_success(post_register(client, follow_redirects=True, password=password))
    assert check_password_hash(get_user("ana@example.com")["password_hash"], password)


def test_tc31_confirm_differs_only_in_case(client):
    response = post_register(client, password="Secret123", confirm_password="secret123")
    assert_rejected(response, "Passwords do not match.")


def test_tc34_success_message_shown_only_once(client):
    assert_success(post_register(client, follow_redirects=True))
    assert not shows(client.get("/login"), SUCCESS)
    assert count_users("ana@example.com") == 1


def test_tc35_resubmitting_after_success_is_duplicate(client):
    assert_success(post_register(client, follow_redirects=True))
    response = post_register(client)
    assert shows(response, DUPLICATE)
    assert count_users("ana@example.com") == 1


def test_tc36_second_insert_of_same_email_raises(client):
    create_user("Ana", "ana@example.com", "Secret123")
    with pytest.raises(EmailTakenError):
        create_user("Ana again", "ana@example.com", "Secret123")
    assert count_users("ana@example.com") == 1


def test_tc37_very_long_name(client):
    response = post_register(client, name="a" * 10_000)
    assert_rejected(response, "Name must be 100 characters or fewer.")


@pytest.mark.parametrize(
    "email", ["ana@", "@example.com", "ana@example", "ana silva@example.com", "ana@@example.com"]
)
def test_tc38_malformed_emails(client, email):
    response = post_register(client, email=email)
    assert_rejected(response, "Please enter a valid email address.", email=email)


def test_tc39_markup_and_sql_like_names_stored_as_text(client):
    for name, email in (("<b>Ana</b>", "b@example.com"), ("' OR 1=1 --", "sql@example.com")):
        assert_success(post_register(client, follow_redirects=True, name=name, email=email))
        assert get_user(email)["name"] == name

    # When re-shown in the form, markup is escaped, not rendered.
    response = post_register(client, name="<b>Ana</b>", email="c@example.com", password="short")
    assert "&lt;b&gt;Ana&lt;/b&gt;" in body(response)
    assert "<b>Ana</b>" not in body(response)
    assert query("SELECT count(*) AS n FROM users")[0]["n"] == 3  # demo + 2


def test_tc40_demo_email_rejected_and_demo_unchanged(client):
    before = get_user(DEMO_EMAIL)
    response = post_register(client, email=DEMO_EMAIL)
    assert shows(response, DUPLICATE)
    after = get_user(DEMO_EMAIL)
    assert after["name"] == before["name"]
    assert after["password_hash"] == before["password_hash"]


def test_tc41_password_equal_to_email_accepted(client):
    response = post_register(client, follow_redirects=True, password="ana@example.com")
    assert_success(response)


# --------------------------------------------------------------------- #
# Permissions                                                            #
# --------------------------------------------------------------------- #

def test_tc42_visitor_can_register(client):
    assert_success(post_register(client, follow_redirects=True, email="ben@example.com"))
    assert count_users("ben@example.com") == 1


def test_tc43_registered_user_cannot_reregister(client):
    assert_success(post_register(client, follow_redirects=True))
    response = post_register(client)
    assert shows(response, DUPLICATE)


def test_tc44_registering_does_not_sign_in(client):
    response = post_register(client, follow_redirects=True)
    html = body(response)
    assert "Get started" in html
    assert "Sign in" in html
    with client.session_transaction() as session:
        assert "user_id" not in session


def test_tc45_password_never_shown_or_stored_readable(client):
    password = "Secret123"
    responses = [
        post_register(client, password=password, confirm_password="Mismatch1"),
        post_register(client, name="", password=password),
        post_register(client, follow_redirects=True, password=password),
    ]
    for response in responses:
        assert password not in body(response)

    stored = get_user("ana@example.com")["password_hash"]
    assert stored != password
    assert password not in stored
    assert check_password_hash(stored, password)


# --------------------------------------------------------------------- #
# Regression (Step 01 and existing pages)                                #
# --------------------------------------------------------------------- #

@pytest.mark.parametrize("path", ["/", "/login", "/terms", "/privacy", "/register"])
def test_tc46_existing_pages_still_load(client, path):
    assert client.get(path).status_code == 200


def test_tc47_demo_data_unchanged_after_registration_and_restart(client):
    from database.db import init_db, seed_db

    assert_success(post_register(client, follow_redirects=True))
    init_db()
    seed_db()
    assert count_users(DEMO_EMAIL) == 1
    demo = get_user(DEMO_EMAIL)
    rows = query("SELECT count(*) AS n FROM expenses WHERE user_id = %s", (demo["id"],))
    assert rows[0]["n"] == 8
    assert count_users("ana@example.com") == 1


@pytest.mark.parametrize(
    "path, text",
    [
        ("/logout", "Logout — coming in Step 3"),
        ("/profile", "Profile page — coming in Step 4"),
        ("/expenses/add", "Add expense — coming in Step 7"),
    ],
)
def test_tc48_placeholders_unchanged(client, path, text):
    assert body(client.get(path)) == text
