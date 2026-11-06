# SecureSpace - API and Route Documentation

## 1. Overview

SecureSpace is a Flask-based secure document-sharing application.

The current implementation uses server-rendered HTML pages and form-based routes. It does not expose a separate REST API or JSON-based public API.

This document describes the application's available routes, HTTP methods, authentication requirements, and authorization rules.

## 2. Authentication

The application uses Flask-Login for session-based authentication.

- Users must log in before accessing protected document operations.
- Passwords are stored using Werkzeug password hashing.
- Newly registered users receive the Viewer role by default.
- Login POST requests are limited to 5 attempts per minute.
- CSRF protection is enabled for application forms.

## 3. Route Reference

### 3.1 Authentication Routes

| Method | Endpoint | Authentication | Description |
|---|---|---|---|
| GET, POST | `/register` | Public | Display registration form and create an account |
| GET, POST | `/login` | Public | Display login form and authenticate a user |
| POST | `/logout` | Public (session optional) | End the current user session if one exists |

Registration assigns the default Viewer role.

### 3.2 General Routes

| Method | Endpoint | Authentication | Authorization | Description |
|---|---|---|---|---|
| GET | `/` | Public | None | Redirect to login |
| GET | `/dashboard` | Required | Authenticated users | Display user dashboard |
| GET | `/admin/activity` | Required | Administrator only | Display the latest 100 audit activities |

Non-administrator users receive HTTP 403 when accessing the administrator activity page.

### 3.3 Document Routes

All document routes use the `/documents` URL prefix.

| Method | Endpoint | Authentication | Authorization | Description |
|---|---|---|---|---|
| GET | `/documents/` | Required | Admin sees all documents; other users see owned or shared documents | List, search, and filter documents |
| GET, POST | `/documents/upload` | Required | Authenticated users | Display upload form and upload documents |
| GET | `/documents/preview/<document_id>` | Required | Owner or user with read/edit access | Preview supported documents |
| GET | `/documents/download/<document_id>` | Required | Owner or user with read/edit access | Download a document |
| POST | `/documents/suggest-permission/<document_id>` | Required | Document owner only | Generate a permission recommendation |
| POST | `/documents/share/<document_id>` | Required | Document owner only | Grant or update read/edit access |
| POST | `/documents/revoke/<document_id>` | Required | Document owner only | Revoke a user's document permission |
| POST | `/documents/edit/<document_id>` | Required | Owner or user with edit permission | Update document category |
| POST | `/documents/delete/<document_id>` | Required | Document owner or administrator | Delete a document |

## 4. Authorization Rules

### Administrator
- Can view all documents in the document listing.
- Can access the administrator activity page.
- Can delete documents.
- Does not automatically receive document preview or download permission unless the access-check logic grants it.

### Document Owner
- Can view and manage owned documents.
- Can upload documents.
- Can share and revoke document permissions.
- Can update document categories and delete owned documents.
- Can use the Permission Advisor.

### Viewer
- Can view documents explicitly shared with them.
- Can preview and download documents with read or edit permission.
- Cannot share, revoke, or delete another user's documents.

### Document-level Editor Permission
- Receives the access granted through a document-level edit permission.
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

## 6. Audit Logging

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
- Key denied document-access attempts.

Audit records include relevant actor, document, action, timestamp, IP address, and details fields.

HMAC-based integrity hashes are used to detect unauthorized changes to audit records.

## 7. Permission Advisor

The Permission Advisor is a rule-based recommendation service.

It considers document category, sharing purpose, and existing permission context to suggest read or edit access.

Recommendations do not grant access automatically. The document owner must explicitly approve access through the sharing operation.

## 8. Security Controls

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

## 9. HTTP Status Codes

The application uses standard HTTP status codes where applicable:

| Status | Meaning |
|---|---|
| 200 | Request completed successfully |
| 302 | Redirect, commonly after form submission |
| 403 | Access denied |
| 404 | Resource not found |
| 429 | Rate limit exceeded |

Some form-based operations communicate results through redirects and flash messages rather than JSON responses.

## 10. Important Implementation Notes

- This documentation describes the active root-level Flask application and its registered blueprints.
- The application currently uses server-rendered pages and form submissions.
- There is no separate REST API authentication mechanism.
- Production deployment and external infrastructure configuration remain pending.


