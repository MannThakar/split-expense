from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
import re
import sys
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash
from database.db import (
    get_db, init_db, seed_db, create_user, get_user_by_email, EmailTakenError,
)

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-only-change-me")


# ------------------------------------------------------------------ #
# Database startup                                                    #
# ------------------------------------------------------------------ #

try:
    init_db()
    seed_db()
except psycopg2.OperationalError:
    print(
        "Could not connect to PostgreSQL. Check that the server is running and "
        "DB_HOST/DB_PORT/DB_NAME/DB_USER/DB_PASSWORD are set correctly.",
        file=sys.stderr,
    )
    sys.exit(1)


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s.]+(\.[^@\s.]+)+$")


def validate_registration(name, email, password, confirm):
    """Returns the first error message in field order, or None if all valid."""
    if not name:
        return "Please enter your full name."
    if len(name) > 100:
        return "Name must be 100 characters or fewer."
    if not email:
        return "Please enter your email address."
    if len(email) > 254:
        return "Email must be 254 characters or fewer."
    if not EMAIL_RE.match(email):
        return "Please enter a valid email address."
    if not password:
        return "Please enter a password."
    if len(password) < 8:
        return "Password must be at least 8 characters."
    if len(password) > 128:
        return "Password must be 128 characters or fewer."
    if not confirm:
        return "Please confirm your password."
    if confirm != password:
        return "Passwords do not match."
    return None


def validate_login(email, password):
    """Returns the first error message in field order, or None if all valid."""
    if not email:
        return "Please enter your email address."
    if len(email) > 254:
        return "Email must be 254 characters or fewer."
    if not EMAIL_RE.match(email):
        return "Please enter a valid email address."
    if not password:
        return "Please enter your password."
    return None


# Compared against when the email has no account, so an unknown email takes
# about as long to reject as a wrong password (BR-1).
_DUMMY_HASH = generate_password_hash("not-a-real-password")


@app.route("/register", methods=["GET", "POST"])
def register():
    if session.get("user_id"):
        return redirect(url_for("profile"))

    if request.method == "GET":
        return render_template("register.html")

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")
    confirm = request.form.get("confirm_password", "")

    error = validate_registration(name, email, password, confirm)
    if error:
        return render_template("register.html", error=error, name=name, email=email)

    try:
        create_user(name, email.lower(), password)
    except EmailTakenError:
        error = "An account with this email already exists. Please sign in instead."
        return render_template("register.html", error=error, name=name, email=email)
    except Exception:
        app.logger.exception("Registration failed")
        error = "We couldn't create your account right now. Please try again in a moment."
        return render_template("register.html", error=error, name=name, email=email)

    flash("Account created. Please sign in.", "success")
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_id"):
        return redirect(url_for("profile"))

    if request.method == "GET":
        return render_template("login.html")

    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    error = validate_login(email, password)
    if error:
        return render_template("login.html", error=error, email=email)

    try:
        user = get_user_by_email(email.lower())
    except Exception:
        app.logger.exception("Sign-in failed")
        error = "We couldn't sign you in right now. Please try again in a moment."
        return render_template("login.html", error=error, email=email)

    password_ok = check_password_hash(user["password_hash"] if user else _DUMMY_HASH, password)
    if not user or not password_ok:
        error = "Incorrect email or password."
        return render_template("login.html", error=error, email=email)

    session.clear()
    session["user_id"] = user["id"]
    return redirect(url_for("profile"))


@app.route("/logout")
def logout():
    if session.get("user_id"):
        session.clear()
        flash("You have been signed out.", "success")
    return redirect(url_for("login"))


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/profile")
def profile():
    return "Profile page — coming in Step 4"


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    app.run(debug=True, port=5001, host="0.0.0.0")
