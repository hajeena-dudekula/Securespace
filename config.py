import os

class Config:

    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "securespace-dev-key-change-before-deployment"
    )

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///securespace.db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

    SESSION_COOKIE_SECURE = (
        os.environ.get("SESSION_COOKIE_SECURE", "false").lower() == "true"
    )

    DOCUMENT_STORAGE_PATH = os.environ.get('DOCUMENT_STORAGE_PATH')
