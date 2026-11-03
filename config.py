import os

class Config:

    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "securespace-dev-key-change-before-deployment"
    )

    SQLALCHEMY_DATABASE_URI = "sqlite:///securespace.db"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
