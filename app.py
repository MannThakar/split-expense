from flask import Flask, render_template, request, redirect, url_for, flash
import os
import re
import sys
import psycopg2
from database.db import get_db, init_db, seed_db, create_user, EmailTakenError

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


@app.route("/register", methods=["GET", "POST"])
def register():
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


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/logout")
def logout():
    return "Logout — coming in Step 3"


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
