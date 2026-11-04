# AI Usage Log – SecureSpace

## Project Overview

**Project:** SecureSpace – Secure Document Sharing with a Real Audit Trail
**Challenge:** Snovasys Fresher Hiring Challenge 2026
**Technology Stack:** Python, Flask, SQLite, HTML, CSS, JavaScript

This document records how AI assistance was used during project planning, implementation, debugging, and review.

AI-generated suggestions were reviewed and adapted to the existing project. They were not treated as automatically correct. Implementation decisions and verification remain the developer's responsibility.

---

## Day 1 – Project Analysis and Planning

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

## Day 2 – Authentication and Initial Security

Date: 2026-11-02

### Entry 1 – User Registration

**Prompt objective:**

Implement user registration in Flask and SQLite using the existing User model and project structure.

**AI assistance summary:**

Received guidance for collecting registration details, hashing passwords, and saving user records.

**Review and corrections:**

- Added input validation.
- Added duplicate username and email checks.
- Used password hashing instead of storing plain-text passwords.
- Registration assigns the default viewer role; users cannot select an administrator role themselves.

### Entry 2 – User Login

**Prompt objective:**

Implement username and password login using Flask-Login.

**AI assistance summary:**

Received guidance for checking submitted credentials against stored password hashes and creating an authenticated session.

**Review and remaining work:**

- Password hash verification is used.
- Login attempt rate limiting has not been implemented.
- Brute-force protection remains a security improvement.

### Entry 3 – Dashboard Access Control

**Prompt objective:**

Protect the dashboard so that only authenticated users can access it.

**AI assistance summary:**

Received guidance for using Flask-Login authentication decorators.

**Review and corrections:**

- Authentication is required for dashboard access.
- Authentication alone is not treated as sufficient authorization for individual documents.
- Document-level access checks were addressed during the document management and authorization stages.

### Entry 4 – Authentication Security Review

**Prompt objective:**

Review the registration and login implementation and identify security gaps.

**AI assistance summary:**

Received guidance about password storage, authentication, and the difference between authentication and authorization.

**Developer decision:**

Document ownership and permission checks were treated as separate requirements and implemented in the later authorization stage.

### Entry 5 – Session and Logout

**Prompt objective:**

Implement logout using Flask-Login and review the logout request method.

**AI assistance summary:**

Received guidance for ending the authenticated session.

**Review and corrections:**

- Logout uses a POST route.
- CSRF protection still needs to be configured and verified.

---

## Day 3 – Document Management

Date: 2026-11-04

### Entry 1 – Document Upload

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

### Entry 2 – Document Listing and Search

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

### Entry 3 – Document Preview and Download

**Prompt objective:**

Implement document preview and download routes with authentication and access checks.

**AI assistance summary:**

Received guidance for serving stored documents through Flask routes.

**Developer review and implementation:**

- Added preview and download routes.
- Added login and document access checks.
- Added activity logging for preview and download actions.

---

## Day 4 – Authorization and Audit Trail

Date: 2026-11-04

### Entry 1 – Document Permission Model

**Prompt objective:**

Design and implement document-level sharing permissions using the existing SQLAlchemy models.

**AI assistance summary:**

Received guidance for associating users with documents and storing permission types.

**Developer review and implementation:**

- Added a DocumentPermission model.
- Added read and edit permission types.
- Added document and user relationships.
- Added database constraints for permission values and duplicate document-user permissions.

### Entry 2 – Share and Revoke Access

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

### Entry 3 – Document Authorization

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

### Entry 4 – Document Management Operations

**Prompt objective:**

Implement document category editing and deletion while preserving authorization checks and activity records.

**AI assistance summary:**

Received implementation and debugging guidance for document modification and deletion routes.

**Developer review and implementation:**

- Added category editing.
- Added document deletion.
- Added owner and administrator checks.
- Recorded document modification and deletion events.

### Entry 5 – Audit Trail

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

### Entry 6 – Debugging and Verification

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

Compilation confirms syntax validity only. Complete end-to-end authorization and security testing is still pending.

---

## Responsible Use of AI

- AI was used as a development and debugging assistant.
- Existing project structure and code were considered before making changes.
- Generated suggestions were reviewed before implementation.
- Reported errors were investigated and corrected.
- Features that have not been implemented or tested are not described as completed.
- Final implementation and testing decisions remain the developer's responsibility.

## Related Project Documentation

- `PROBLEM_STATEMENT.md` – Project requirements.
- `THREATS.md` – Security threat analysis and mitigation status.
- `AI_TOOLS.md` – AI tools and usage information.
- `PROJECT_PLAN.md` – Development progress and planned work.
- `PROMPTS.md` – AI assistance and development review log.
