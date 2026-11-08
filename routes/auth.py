from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
import re
import secrets
import smtplib
import ssl
from email.message import EmailMessage
from itsdangerous import URLSafeTimedSerializer, BadSignature

from extensions import db, limiter, oauth
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




def get_reset_serializer(user=None):
    return URLSafeTimedSerializer(
        current_app.config["SECRET_KEY"],
        salt="securespace-password-reset"
    )


def send_password_reset_email(user, token):
    reset_url = url_for(
        "auth.reset_password",
        token=token,
        _external=True
    )

    config = current_app.config

    if not config.get("MAIL_SERVER") or not config.get("MAIL_DEFAULT_SENDER"):
        if config.get("APP_ENV", "development") != "production":
            current_app.logger.warning(
                "Development password reset link for %s: %s",
                user.email,
                reset_url
            )
            return True

        current_app.logger.error("Password reset email is not configured.")
        return False

    message = EmailMessage()
    message["Subject"] = "SecureSpace Password Reset"
    message["From"] = config["MAIL_DEFAULT_SENDER"]
    message["To"] = user.email
    message.set_content(
        "We received a request to reset your SecureSpace password.\n\n"
        f"Use this link within 30 minutes:\n{reset_url}\n\n"
        "If you did not request this, ignore this email."
    )

    try:
        with smtplib.SMTP(
            config["MAIL_SERVER"],
            config.get("MAIL_PORT", 587),
            timeout=15
        ) as server:
            server.ehlo()

            if config.get("MAIL_USE_TLS", True):
                server.starttls(context=ssl.create_default_context())
                server.ehlo()

            if config.get("MAIL_USERNAME") and config.get("MAIL_PASSWORD"):
                server.login(
                    config["MAIL_USERNAME"],
                    config["MAIL_PASSWORD"]
                )

            server.send_message(message)

        return True

    except Exception:
        current_app.logger.exception("Password reset email delivery failed.")
        return False


@auth.route("/forgot-password", methods=["GET", "POST"])
@limiter.limit("5 per minute", methods=["POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()

        if email:
            account = User.query.filter_by(email=email).first()

            if account:
                token = get_reset_serializer().dumps({
                    "user_id": account.id,
                    "password_hash": account.password
                })
                send_password_reset_email(account, token)

        flash(
            "If an account exists for that email, password reset instructions "
            "will be sent."
        )
        return redirect(url_for("auth.forgot_password"))

    return render_template("forgot_password.html")


@auth.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    account = None

    try:
        data = get_reset_serializer().loads(
            token,
            max_age=current_app.config.get(
                "PASSWORD_RESET_TOKEN_MAX_AGE", 1800
            )
        )

        account = db.session.get(User, int(data["user_id"]))

        if account is None or data.get("password_hash") != account.password:
            raise BadSignature("Invalid or already-used reset token")

    except (BadSignature, KeyError, TypeError, ValueError):
        flash("This password reset link is invalid or has expired.")
        return redirect(url_for("auth.forgot_password"))

    if request.method == "POST":
        password = request.form.get("password", "")
        password_error = validate_password_strength(password)

        if password_error:
            flash(password_error)
            return render_template("reset_password.html", token=token)

        account.password = generate_password_hash(password)
        db.session.commit()

        flash("Password reset successful. Please login.")
        return redirect(url_for("auth.login"))

    return render_template("reset_password.html", token=token)


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

            remember = request.form.get("remember") == "on"
            login_user(account, remember=remember)

            return redirect(url_for("dashboard"))

        flash("Invalid username or password.")

    return render_template("login.html")


@auth.route("/logout", methods=["POST"])
def logout():

    logout_user()

    return redirect(url_for("auth.login"))



@auth.route("/login/google")
def google_login():
    if not current_app.config.get("GOOGLE_CLIENT_ID") or not current_app.config.get("GOOGLE_CLIENT_SECRET"):
        flash("Google sign-in is not configured. Please use username and password.")
        return redirect(url_for("auth.login"))

    client = oauth.create_client("google")

    if client is None:
        flash("Google sign-in is temporarily unavailable.")
        return redirect(url_for("auth.login"))

    redirect_uri = current_app.config.get("GOOGLE_REDIRECT_URI") or url_for(
        "auth.google_callback",
        _external=True
    )

    return client.authorize_redirect(redirect_uri)


@auth.route("/login/google/callback")
def google_callback():
    client = oauth.create_client("google")

    if client is None:
        flash("Google sign-in is not configured.")
        return redirect(url_for("auth.login"))

    try:
        token = client.authorize_access_token()
        user_info = token.get("userinfo")

        if not user_info:
            flash("Google did not provide verified account information.")
            return redirect(url_for("auth.login"))

        email = (user_info.get("email") or "").strip().lower()

        if not email or user_info.get("email_verified") is not True:
            flash("Please use a Google account with a verified email address.")
            return redirect(url_for("auth.login"))

        account = User.query.filter_by(email=email).first()

        if account is None:
            base_username = re.sub(
                r"[^A-Za-z0-9_.-]",
                "",
                email.split("@")[0]
            )[:60] or "googleuser"

            username = base_username

            while User.query.filter_by(username=username).first():
                username = f"{base_username[:60]}_{secrets.token_hex(3)}"

            account = User(
                username=username,
                email=email,
                password=generate_password_hash(secrets.token_urlsafe(48)),
                role="viewer"
            )

            db.session.add(account)
            db.session.commit()

        login_user(account)
        return redirect(url_for("dashboard"))

    except Exception:
        db.session.rollback()
        current_app.logger.exception("Google sign-in failed.")
        flash("Google sign-in failed. Please try again.")
        return redirect(url_for("auth.login"))
