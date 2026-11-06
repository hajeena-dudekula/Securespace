import os

from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

db = SQLAlchemy()

app_env = os.environ.get("APP_ENV", "development").lower()

rate_limit_storage = os.environ.get(
    "RATELIMIT_STORAGE_URI",
    "memory://"
)

if app_env == "production" and rate_limit_storage.startswith("memory://"):
    raise RuntimeError(
        "Production requires Redis for persistent rate-limit storage."
    )

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[],
    storage_uri=rate_limit_storage
)
