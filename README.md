# SecureSpace
### Secure Document Sharing with a Verifiable Audit Trail

SecureSpace is a secure document management and sharing platform developed for the **Snovasys Fresher Hiring Challenge 2026**. It enables users to securely upload, manage, share, and access documents through role-based authorization while maintaining tamper-evident activity records.

## Project Status

**COMPLETED**

## Key Features

- Secure user registration, login, logout, and session management.
- Role-based access control: Administrator, Document Owner, and Viewer.
- Secure document upload, preview, download, and editing.
- Document-level read and edit permissions.
- Owner-controlled document sharing and access revocation.
- Document search and category filtering.
- Admin dashboard with owner and date-based filtering.
- Activity history with document and account-related events.
- Audit logs with HMAC-based tamper-evident integrity verification.
- Rule-based AI Permission Advisor with owner approval.
- Login rate limiting and CSRF protection.
- Document sharing timestamps and activity history.
- Responsive web interface.

## Technology Stack

| Component | Technology |
|---|---|
| Backend | Python, Flask |
| Database | Flask-SQLAlchemy, SQLite / PostgreSQL configuration |
| Authentication | Flask-Login, Werkzeug |
| Security | Flask-WTF, Flask-Limiter |
| Frontend | HTML, CSS, JavaScript, Bootstrap |
| Audit Integrity | HMAC |
| Cache / Rate Limiting | Redis |
| Testing | Pytest |
| Deployment | Render, Gunicorn |

## Security Implementation

- Secure password hashing using Werkzeug.
- Server-side authorization checks for document operations.
- Private document storage.
- UUID-based stored filenames.
- File extension and content-signature validation.
- CSRF protection for form submissions.
- Login rate limiting.
- HMAC-based audit record integrity verification.
- Permission checks for document viewing, editing, downloading, and sharing.
- Owner approval required before suggested permissions are granted.

## AI Permission Advisor

SecureSpace includes a rule-based Permission Advisor that evaluates document-sharing context and suggests suitable access permissions.

- Provides permission recommendations.
- Supports owner review and approval.
- Does not automatically grant access.
- Keeps final permission decisions under document-owner control.

## Installation and Setup

Clone the repository:

    git clone https://github.com/hajeena-dudekula/Securespace.git
    cd Securespace

Create a virtual environment:

    python -m venv venv

Activate it in Windows PowerShell:

    .\venv\Scripts\Activate.ps1

Install dependencies:

    python -m pip install -r requirements.txt

Configure the required environment variables in a local `.env` file.

Run the application:

    python run.py

Open:

    http://127.0.0.1:5000

## Automated Testing

Run the test suite:

    python -m pytest -q

**Latest verified test result:**

    78 passed
    0 failed

The test suite covers authentication, authorization, document operations, permissions, and security-related application behavior.

## Environment Variables

Configure the following variables according to the deployment environment:

- `SECRET_KEY` â€“ Flask application secret.
- `AUDIT_LOG_SECRET` â€“ Audit integrity signing secret.
- `DATABASE_URL` â€“ Database connection URL.
- `APP_ENV` â€“ Application environment.
- `RATELIMIT_STORAGE_URI` â€“ Rate-limit storage backend.
- `DOCUMENT_STORAGE_PATH` â€“ Private document storage directory.

Never commit production secrets, `.env` files, database files, or private uploaded documents.

## Deployment

**Platform:** Render
**Repository:** https://github.com/hajeena-dudekula/Securespace
**Production URL:** https://securespace-new.onrender.com

The application uses Gunicorn as its production application server.

## Project Documentation

- `API.md` â€“ Application routes and access permissions.
- `THREATS.md` â€“ Security threats, mitigations, and accepted risks.
- `PROMPTS.md` â€“ AI-assisted development history.
- `PROJECT_PLAN.md` â€“ Project architecture and development plan.
- `PROBLEM_STATEMENT.md` â€“ Original project problem statement.

## Repository

GitHub: https://github.com/hajeena-dudekula/Securespace

---

**SecureSpace â€“ Secure Documents. Controlled Access. Verifiable Activity.**
