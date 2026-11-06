# AI Usage Log â€“ SecureSpace

## Project Overview

**Project:** SecureSpace â€“ Secure Document Sharing with a Real Audit Trail
**Challenge:** Snovasys Fresher Hiring Challenge 2026
**Technology Stack:** Python, Flask, SQLite, HTML, CSS, JavaScript

This document records how AI assistance was used during project planning, implementation, debugging, and review.

AI-generated suggestions were reviewed and adapted to the existing project. They were not treated as automatically correct. Implementation decisions and verification remain the developer's responsibility.

---

## Day 1 â€“ Project Analysis and Planning

### Prompt 1: Project Analysis and Planning

**Prompt objective:**

Analyze the SecureSpace project requirements and help plan a secure document-sharing application suitable for a beginner developer.

The requested guidance covered:

1. Main application features.
2. User roles and permissions.
3. Security requirements and possible threats.
4. Database tables and relationships.
5. Project architecture and folder structure.
6. A step-by-step development plan.
7. Mandatory and optional requirements.
8. Evaluation and project quality considerations.

**AI assistance summary:**

AI assistance was used to understand the project scope and explore an application architecture involving authentication, document management, access permissions, and audit logging.

**Developer review and decisions:**

- Reviewed the suggestions against the project requirements.
- Selected Flask and SQLite for the backend.
- Prioritized authentication, document management, authorization, and audit logging.
- Planned development in manageable stages.

---

## Day 2 â€“ Authentication and Initial Security

Date: 2026-11-02

### Entry 1 â€“ User Registration

**Prompt objective:**

Implement user registration in Flask and SQLite using the existing User model and project structure.

**AI assistance summary:**

Received guidance for collecting registration details, hashing passwords, and saving user records.

**Review and corrections:**

- Added input validation.
- Added duplicate username and email checks.
- Used password hashing instead of storing plain-text passwords.
- Registration assigns the default viewer role; users cannot select an administrator role themselves.

### Entry 2 â€“ User Login

**Prompt objective:**

Implement username and password login using Flask-Login.

**AI assistance summary:**

Received guidance for checking submitted credentials against stored password hashes and creating an authenticated session.

**Review and remaining work:**

- Password hash verification is used.
- At this stage, login attempt rate limiting had not yet been implemented. It was added and tested during Day 6.
- Additional brute-force protections beyond the implemented login rate limit remain a possible security improvement.

### Entry 3 â€“ Dashboard Access Control

**Prompt objective:**

Protect the dashboard so that only authenticated users can access it.

**AI assistance summary:**

Received guidance for using Flask-Login authentication decorators.

**Review and corrections:**

- Authentication is required for dashboard access.
- Authentication alone is not treated as sufficient authorization for individual documents.
- Document-level access checks were addressed during the document management and authorization stages.

### Entry 4 â€“ Authentication Security Review

**Prompt objective:**

Review the registration and login implementation and identify security gaps.

**AI assistance summary:**

Received guidance about password storage, authentication, and the difference between authentication and authorization.

**Developer decision:**

Document ownership and permission checks were treated as separate requirements and implemented in the later authorization stage.

### Entry 5 â€“ Session and Logout

**Prompt objective:**

Implement logout using Flask-Login and review the logout request method.

**AI assistance summary:**

Received guidance for ending the authenticated session.

**Review and corrections:**

- Logout uses a POST route.
- At this stage, CSRF protection was not yet configured. It was added to relevant forms and tested during Day 6.

---

## Day 3 â€“ Document Management

Date: 2026-11-04

### Entry 1 â€“ Document Upload

**Prompt objective:**

Implement secure document uploading using the existing Flask application structure.

**AI assistance summary:**

Received guidance for handling uploaded files, validating extensions, storing files, and creating database records.

**Developer review and implementation:**

- Added support for PDF, DOCX, TXT, PNG, JPG, and JPEG.
- Added file-size limits based on file type.
- Used secure filename handling.
- Used UUID-based stored filenames.
- Stored uploaded files in the application instance document folder.
- Added upload success and error messages.

### Entry 2 â€“ Document Listing and Search

**Prompt objective:**

Implement document listing with filename search, category filtering, and upload date display.

**AI assistance summary:**

Received guidance for querying document records and displaying them in the application.

**Developer review and implementation:**

- Added document listing.
- Added filename search.
- Added category filtering.
- Added categories: General, Personal, Work, Education, and Finance.
- Added upload-date ordering and IST display.

### Entry 3 â€“ Document Preview and Download

**Prompt objective:**

Implement document preview and download routes with authentication and access checks.

**AI assistance summary:**

Received guidance for serving stored documents through Flask routes.

**Developer review and implementation:**

- Added preview and download routes.
- Added login and document access checks.
- Added activity logging for preview and download actions.

---

## Day 4 â€“ Authorization and Audit Trail

Date: 2026-11-04

### Entry 1 â€“ Document Permission Model

**Prompt objective:**

Design and implement document-level sharing permissions using the existing SQLAlchemy models.

**AI assistance summary:**

Received guidance for associating users with documents and storing permission types.

**Developer review and implementation:**

- Added a DocumentPermission model.
- Added read and edit permission types.
- Added document and user relationships.
- Added database constraints for permission values and duplicate document-user permissions.

### Entry 2 â€“ Share and Revoke Access

**Prompt objective:**

Implement document sharing with registered users and allow document owners to revoke access.

**AI assistance summary:**

Received guidance for validating target users, assigning permissions, and removing existing permissions.

**Developer review and implementation:**

- Added sharing using usernames.
- Validated read and edit permission values.
- Prevented users from sharing documents with themselves.
- Allowed existing permissions to be updated.
- Added permission revocation.
- Added audit events for granting and revoking permissions.

### Entry 3 â€“ Document Authorization

**Prompt objective:**

Review document routes and enforce ownership and permission checks before allowing document operations.

**AI assistance summary:**

Received guidance for centralizing document access checks and distinguishing owners, administrators, and shared users.

**Developer review and implementation:**

- Added a document access helper.
- Owners and administrators receive edit access.
- Shared users receive the permission assigned to them.
- Preview and download routes check document access.
- Document modifications require appropriate edit access.
- Document deletion is restricted to the owner or administrator.

### Entry 4 â€“ Document Management Operations

**Prompt objective:**

Implement document category editing and deletion while preserving authorization checks and activity records.

**AI assistance summary:**

Received implementation and debugging guidance for document modification and deletion routes.

**Developer review and implementation:**

- Added category editing.
- Added document deletion.
- Added owner and administrator checks.
- Recorded document modification and deletion events.

### Entry 5 â€“ Audit Trail

**Prompt objective:**

Design an audit log that records important document activities and provides an administrator activity view.

**AI assistance summary:**

Received guidance for recording the actor, document reference, action, details, IP address, and timestamp.

**Developer review and implementation:**

- Added an AuditLog model.
- Added logging for upload, preview, download, permission grant, permission revocation, modification, and deletion.
- Added an administrator activity route.
- Restricted the activity page to administrator accounts.
- Added a dashboard link to the activity page.

### Entry 6 â€“ Debugging and Verification

**Prompt objective:**

Help investigate errors in document routes, database relationships, category filtering, and deletion logic.

**AI assistance summary:**

Received debugging guidance based on the reported errors and existing source code.

**Developer review and verification:**

- Corrected the document category filtering logic.
- Addressed a foreign-key issue when recording document deletion.
- Ran Python compilation checks on the relevant application and route files.
- Compilation completed without syntax errors.

**Verification limitation:**

Compilation confirms syntax validity only. At this development stage, complete end-to-end authorization and security testing was still pending. This was subsequently addressed during Day 6, when the full test suite completed with 52 passing tests.

---

## Responsible Use of AI

- AI was used as a development and debugging assistant.
- Existing project structure and code were considered before making changes.
- Generated suggestions were reviewed before implementation.
- Reported errors were investigated and corrected.
- Features that have not been implemented or tested are not described as completed.
- Final implementation and testing decisions remain the developer's responsibility.

## Related Project Documentation

- `PROBLEM_STATEMENT.md` â€“ Project requirements.
- `THREATS.md` â€“ Security threat analysis and mitigation status.
- `AI_TOOLS.md` â€“ AI tools and usage information.
- `PROJECT_PLAN.md` â€“ Development progress and planned work.
- `PROMPTS.md` â€“ AI assistance and development review log.

### Entry 7 â€“ Deployment Configuration Preparation (November 5, 2026)

**Prompt objective:**

Prepare the Flask application for deployment by supporting environment-based configuration and configurable document storage.

**AI assistance summary:**

Received guidance to update application configuration and centralize document storage path handling without disturbing existing document operations.

**Developer review and implementation:**

- Added environment-variable support for SECRET_KEY, DATABASE_URL, SESSION_COOKIE_SECURE, and DOCUMENT_STORAGE_PATH.
- Added a centralized document storage path helper.
- Updated upload, preview, download, and delete operations to use the helper.
- Ran syntax verification.
- Ran the full test suite: 18 passed, 0 failed.
- Committed and pushed the application changes to GitHub.

**Verification limitations:**

Actual deployment, production database setup, persistent storage configuration, production secret enforcement, and live verification remain incomplete. The development SECRET_KEY fallback has not yet been removed.


---

## Day 6 â€“ Security Hardening and Advanced Features

Date: 2026-11-06

### Entry 1 â€“ Login Rate Limiting and CSRF Protection

**Prompt objective:**

Review the existing Flask authentication and document management forms. Identify ways to reduce repeated login attempts and protect state-changing requests against CSRF attacks without breaking existing functionality.

**AI assistance summary:**

Received implementation and debugging guidance for Flask-Limiter and Flask-WTF CSRF protection.

**Developer review and implementation:**

- Added login rate limiting.
- Configured a limit of five login attempts per minute.
- Added CSRF protection to relevant POST forms.
- Added tests for login rate limiting and CSRF rejection.
- Ran the full test suite to check existing functionality.

### Entry 2 â€“ File Upload Security

**Prompt objective:**

Review the existing document upload implementation and identify risks involving file extensions, file content, filenames, and storage paths.

**AI assistance summary:**

Received guidance for file signature checks, safe filenames, UUID-based storage names, and private file storage.

**Developer review and implementation:**

- Added file content signature validation for supported formats.
- Used secure filename handling and UUID-based stored filenames.
- Added upload security tests.
- Checked private storage and unauthorized file access behaviour.

**Verification note:**

File signature checks provide an additional validation layer; they are not a replacement for complete file-format security scanning.

### Entry 3 â€“ Document Search and Filters

**Prompt objective:**

Extend document filtering to support owner and upload-date filters while preserving existing document visibility and authorization rules.

**AI assistance summary:**

Received guidance for updating SQLAlchemy queries and applying date boundaries consistently.

**Developer review and implementation:**

- Added owner filtering for administrators.
- Prevented non-administrator users from using the owner filter to access other users' documents.
- Added date-from and date-to filters.
- Added tests for document filtering.

### Entry 4 â€“ Audit Log Integrity

**Prompt objective:**

Review the existing audit log and explore a way to detect unauthorized modification of stored audit records.

**AI assistance summary:**

Received guidance for creating a hash-linked audit record sequence using HMAC and SHA-256.

**Developer review and implementation:**

- Added an integrity hash field to audit records.
- Implemented HMAC-based audit record signing.
- Linked each record to the previous record's hash.
- Added audit-chain verification logic.
- Backfilled existing audit records.
- Added audit integrity tests.
- Verified the existing audit chain.

**Security consideration:**

The implementation provides tamper-evident verification. It is not claimed to be completely tamper-proof against an attacker who can control the database and signing secret.

### Entry 5 â€“ Permission Advisor

**Prompt objective:**

Explore a permission suggestion feature that helps document owners decide whether a user should receive Read or Edit access.

**AI assistance summary:**

Received guidance for implementing an explainable, purpose-based permission recommendation mechanism.

**Developer review and implementation:**

- Added a separate Permission Advisor service.
- Used the document category and stated purpose to recommend Read or Edit access.
- Added explanations for the recommendations.
- Kept final permission approval with the document owner.
- Did not automatically grant or change permissions.
- Added tests for recommendation logic and route authorization.

**Implementation clarification:**

The current Permission Advisor is a rule-based recommendation engine. It is not represented as an integrated machine-learning or external LLM model.

### Entry 6 â€“ Authorization and Security Test Review

**Prompt objective:**

Review document routes for unauthorized operations and add tests covering access denial, permission boundaries, and audit recording.

**AI assistance summary:**

Received debugging and test-design guidance for owner, viewer, editor, and administrator access scenarios.

**Developer review and verification:**

- Reviewed document access restrictions.
- Added and updated authorization tests.
- Checked denied document operations and security-event logging.
- Verified Permission Advisor owner restrictions.
- Ran the complete test suite.

**Latest verification result:**

52 passed, 12 warnings, 0 failed.

The remaining warnings relate to SQLAlchemy Query.get() deprecation.

### Entry 7 â€“ Production Configuration Review

**Prompt objective:**

Review the deployment configuration, application entrypoint, secret handling, and rate-limit storage requirements before production deployment.

**AI assistance summary:**

Received guidance for separating development and production configuration, validating production secrets, correcting the WSGI entrypoint, and requiring persistent rate-limit storage.

**Developer review and implementation:**

- Added production checks for SECRET_KEY and AUDIT_LOG_SECRET.
- Added minimum secret-length validation.
- Enabled secure session cookies in production.
- Updated run.py to load the root app.py implementation explicitly.
- Added Gunicorn and Redis to requirements.txt.
- Added production enforcement to prevent memory-based rate limiting.
- Ran Python syntax checks and the full test suite.

**Verification limitations:**

- A production Redis service has not yet been connected.
- Actual production deployment has not been completed.
- Production database and persistent document storage still require configuration.
- Live deployment verification remains pending.
