from datetime import timedelta
import os
from dotenv import load_dotenv

load_dotenv()


class Config:

    APP_ENV = os.environ.get("APP_ENV", "development").lower()

    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "securespace-dev-key-change-before-deployment"
    )

    AUDIT_LOG_SECRET = os.environ.get(
        "AUDIT_LOG_SECRET",
        SECRET_KEY
    )

    if APP_ENV == "production":

        if not os.environ.get("SECRET_KEY"):
            raise RuntimeError("Production requires SECRET_KEY.")

        if not os.environ.get("AUDIT_LOG_SECRET"):
            raise RuntimeError("Production requires AUDIT_LOG_SECRET.")

        if len(SECRET_KEY) < 32 or len(AUDIT_LOG_SECRET) < 32:
            raise RuntimeError("Production secrets must be at least 32 characters.")

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///securespace.db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Maximum total request size for document uploads (50 MB)
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024

    REMEMBER_COOKIE_DURATION = timedelta(days=30)
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SAMESITE = "Lax"

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

    SESSION_COOKIE_SECURE = (
        APP_ENV == "production"
        or os.environ.get("SESSION_COOKIE_SECURE", "false").lower() == "true"
    )

    REMEMBER_COOKIE_SECURE = SESSION_COOKIE_SECURE

    DOCUMENT_STORAGE_PATH = os.environ.get("DOCUMENT_STORAGE_PATH")

    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", "587"))
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", "true").lower() == "true"
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER")

    PASSWORD_RESET_TOKEN_MAX_AGE = 1800


    # Google OAuth
    GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
    GOOGLE_REDIRECT_URI = os.environ.get("GOOGLE_REDIRECT_URI")

