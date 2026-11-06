from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from extensions import db, limiter
from models.user import User

auth = Blueprint("auth", __name__)


@auth.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not username or not email or not password:
            flash("Please fill all required fields.")
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
            role="viewer"
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
