# SecureSpace

SecureSpace is a secure document-sharing platform developed for the Snovasys Fresher Hiring Challenge 2026.

## Key Features

- User registration, login, and logout.
- Admin, Owner, and Viewer roles.
- Secure document upload, preview, and download.
- Document-level read and edit permissions.
- Owner-controlled sharing and revocation.
- Document search by name and category.
- Admin owner filtering and date filtering.
- Audit logs with HMAC-based tamper-evident integrity verification.
- Rule-based Permission Advisor requiring owner approval.
- Login rate limiting and CSRF protection.

## Technology Stack

- Python, Flask, Flask-SQLAlchemy
- Flask-Login, Flask-WTF, Flask-Limiter
- SQLite
- HTML, CSS, JavaScript
- Pytest

## Security

- Werkzeug password hashing.
- Server-side document authorization.
- Private storage and UUID-based filenames.
- File extension and content-signature validation.
- CSRF protection and login rate limiting.
- HMAC-signed audit records.

The Permission Advisor provides rule-based suggestions only. It never grants permissions automatically.

## Setup

Clone the repository:

    git clone https://github.com/hajeena-dudekula/Securespace.git
    cd Securespace

Create a virtual environment:

    python -m venv venv

Activate it in Windows PowerShell:

    .\venv\Scripts\Activate.ps1

Install dependencies:

    python -m pip install -r requirements.txt

Run the application:

    python run.py

Open http://127.0.0.1:5000 in your browser.

## Tests

Run:

    python -m pytest

Latest recorded result: 52 passed, 0 failed.

## Environment Variables

- SECRET_KEY: Flask application secret.
- AUDIT_LOG_SECRET: Audit integrity signing secret.
- DATABASE_URL: Database connection URL.
- APP_ENV: Application environment.
- RATELIMIT_STORAGE_URI: Rate-limit storage backend.
- DOCUMENT_STORAGE_PATH: Private document storage directory.

Production requires strong secrets and a persistent Redis rate-limit backend.

## Documentation

- API.md: Application routes and access permissions.
- THREATS.md: Security threats and mitigations.
- PROMPTS.md: AI-assisted development history.
- PROJECT_PLAN.md: Development plan and progress.

## Deployment Status

Production deployment is pending. A production database, persistent private storage, Redis service, and HTTPS configuration must be set up and verified before release.

Core application features and the current automated security test suite have been implemented. Final production verification remains.
