import os


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

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

    SESSION_COOKIE_SECURE = (
        APP_ENV == "production"
        or os.environ.get("SESSION_COOKIE_SECURE", "false").lower() == "true"
    )

    DOCUMENT_STORAGE_PATH = os.environ.get("DOCUMENT_STORAGE_PATH")
