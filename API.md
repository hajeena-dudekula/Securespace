# SecureSpace - API and Route Documentation

## 1. Overview

SecureSpace is a Flask-based secure document-sharing platform developed for the Snovasys Fresher Hiring Challenge 2026.

The application uses server-rendered HTML pages and form-based routes. It does not expose a separate public REST or JSON API.

This document describes the application's routes, HTTP methods, authentication requirements, authorization rules, and security behavior.

## 2. Authentication

SecureSpace uses Flask-Login for session-based authentication.

- Users must authenticate before accessing protected document operations.
- Passwords are stored using Werkzeug password hashing.
- Newly registered users receive the Viewer role by default.
- Login POST requests are rate-limited to 5 attempts per minute.
- CSRF protection is enabled for application forms.
- User sessions are managed through Flask-Login.

## 3. Route Reference

### 3.1 Authentication Routes

| Method | Endpoint | Authentication | Description |
|---|---|---|---|
| GET, POST | `/register` | Public | Display registration form and create an account |
| GET, POST | `/login` | Public | Display login form and authenticate a user |
| POST | `/logout` | Session optional | End the current user session |

New registrations receive the default Viewer role.

### 3.2 General Routes

| Method | Endpoint | Authentication | Authorization | Description |
|---|---|---|---|---|
| GET | `/` | Public | None | Redirect to login |
| GET | `/dashboard` | Required | Authenticated users | Display the appropriate dashboard |
| GET | `/admin/activity` | Required | Administrator only | Display recent audit activities |

Unauthorized access to administrator-only pages is rejected.

### 3.3 Document Routes

All document routes use the `/documents` URL prefix.

| Method | Endpoint | Authentication | Authorization | Description |
|---|---|---|---|---|
| GET | `/documents/` | Required | Admin sees all; other users see owned or shared documents | List, search, and filter documents |
| GET, POST | `/documents/upload` | Required | Authenticated users | Display upload form and upload documents |
| GET | `/documents/preview/<document_id>` | Required | Owner or user with read/edit access | Preview supported documents |
| GET | `/documents/download/<document_id>` | Required | Owner or user with read/edit access | Download a document |
| POST | `/documents/suggest-permission/<document_id>` | Required | Document owner only | Generate a permission recommendation |
| POST | `/documents/share/<document_id>` | Required | Document owner only | Grant or update document access |
| POST | `/documents/revoke/<document_id>` | Required | Document owner only | Revoke document access |
| POST | `/documents/edit/<document_id>` | Required | Owner or user with edit permission | Update document category |
| POST | `/documents/delete/<document_id>` | Required | Document owner or administrator | Delete a document |

### 3.4 Activity and History

The application provides activity-history views to help users review relevant document and account activities. Administrator activity access is restricted to the Administrator role.

## 4. Authorization Rules

### Administrator

- Can view all documents in the document listing.
- Can access administrator activity records.
- Can delete documents.
- Does not automatically receive document preview or download permission unless the document access-check logic grants it.

### Document Owner

- Can view and manage owned documents.
- Can upload documents.
- Can share documents and revoke permissions.
- Can update document categories and delete owned documents.
- Can use the Permission Advisor.
- Retains control over sharing decisions.

### Viewer

- Can view documents explicitly shared with them.
- Can preview and download documents with read or edit permission.
- Cannot share, revoke, or delete another user's documents.

### Document-level Editor Permission

- Receives access through an explicit document-level edit permission.
- Can preview and download the shared document.
- Can update its category.
- Cannot automatically share or delete the document.

## 5. Document Upload Validation

The upload process includes:

- Filename sanitization.
- Allowed file-extension checks.
- Unique stored filenames generated using UUID.
- File-size validation.
- File-content signature validation.
- Private document storage.

Supported extensions include PDF, DOCX, TXT, PNG, JPG, and JPEG.

## 6. Document Sharing and Revocation

- Document owners select users and access levels when sharing.
- Permissions are enforced on the server.
- Owners can revoke previously granted access.
- Sharing timestamps are associated with permission grants.
- Re-sharing updates the permission grant timestamp.
- Users without valid access are denied document operations.

## 7. Audit Logging

Important document and permission operations generate audit records.

Recorded activities include:

- Document upload.
- Document preview.
- Document download.
- Document modification.
- Document deletion.
- Permission grant.
- Permission revocation.
- Permission recommendation generation.
- Denied document-access attempts.

Audit records include relevant actor, document, action, timestamp, IP address, and details fields.

HMAC-based integrity hashes help detect unauthorized modifications to audit records.

## 8. Permission Advisor

The Permission Advisor is a rule-based recommendation service.

It considers document category, sharing purpose, and existing permission context to suggest read or edit access.

- Recommendations are advisory only.
- The owner reviews the suggested access.
- The owner must explicitly approve sharing.
- Permissions are never granted automatically by the advisor.

## 9. Security Controls

- Session-based authentication.
- Server-side document authorization.
- Document-level permission checks.
- CSRF protection.
- Login rate limiting.
- Secure password hashing.
- Filename sanitization.
- File-content validation.
- Private file storage.
- HMAC-based audit integrity verification.

## 10. HTTP Status Codes

| Status | Meaning |
|---|---|
| 200 | Request completed successfully |
| 302 | Redirect, commonly after form submission |
| 403 | Access denied |
| 404 | Resource not found |
| 429 | Rate limit exceeded |

Form-based operations commonly communicate results through redirects and flash messages rather than JSON responses.

## 11. Deployment

- Hosting platform: Render
- Application server: Gunicorn
- Runtime: Python
- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn run:app`
- Source repository: https://github.com/hajeena-dudekula/Securespace
- Deployment URL: https://securespace-new.onrender.com

Production configuration uses environment variables for application secrets, database connectivity, rate-limit storage, and private document storage.

## 12. Testing

Automated tests are executed using Pytest.

Latest locally verified result:

    78 passed
    0 failed

The test suite covers authentication and application functionality, including document and permission-related behavior.

## 13. Implementation Notes

- This documentation describes the active root-level Flask application and its registered blueprints.
- The application uses server-rendered pages and form submissions.
- There is no separate REST API authentication mechanism.
- Document authorization is enforced on the server.
- Permission recommendations require explicit owner approval.

---

**SecureSpace - Secure Documents. Controlled Access. Verifiable Activity.**
