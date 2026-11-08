from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
import re

from extensions import db, limiter
from models.user import User

auth = Blueprint("auth", __name__)


COMMON_PASSWORDS = {
    "password", "password123", "password1234",
    "12345678", "123456789", "qwerty123",
    "admin123", "welcome123", "letmein123"
}


def validate_password_strength(password):
    if len(password) < 8:
        return "Password must contain at least 8 characters."

    if len(password) > 128:
        return "Password must not exceed 128 characters."

    if password.casefold() in COMMON_PASSWORDS:
        return "This password is too common. Choose a stronger password."

    if not re.search(r"[A-Z]", password):
        return "Add at least one uppercase letter."

    if not re.search(r"[a-z]", password):
        return "Add at least one lowercase letter."

    if not re.search(r"[0-9]", password):
        return "Add at least one number."

    if not re.search(r"[^A-Za-z0-9]", password):
        return "Add at least one special character."

    return None


@auth.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        role = request.form.get("role", "viewer").strip().lower()

        if not username or not email or not password:
            flash("Please fill all required fields.")
            return redirect(url_for("auth.register"))

        password_error = validate_password_strength(password)
        if password_error:
            flash(password_error)
            return redirect(url_for("auth.register"))

        if role not in {"owner", "viewer"}:
            flash("Please select a valid account role.")
            return redirect(url_for("auth.register"))

        existing_user = User.query.filter(
            (User.username == username) |
            (User.email == email)
        ).first()

        if existing_user:
            flash("Username or email already exists.")
            return redirect(url_for("auth.register"))

        account = User(
            username=username,
            email=email,
            password=generate_password_hash(password),
            role=role
        )

        db.session.add(account)
        db.session.commit()

        flash("Registration successful! Please login.")
        return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth.route("/login", methods=["GET", "POST"])
@limiter.limit("5 per minute", methods=["POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        account = User.query.filter_by(username=username).first()

        if account and check_password_hash(account.password, password):

            login_user(account)

            return redirect(url_for("dashboard"))

        flash("Invalid username or password.")

    return render_template("login.html")


@auth.route("/logout", methods=["POST"])
def logout():

    logout_user()

    return redirect(url_for("auth.login"))
