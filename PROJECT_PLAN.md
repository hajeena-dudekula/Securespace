## Current Progress

- Day 1: Project setup completed.
- Day 2: User authentication implementation completed.
- Day 3: Document management implementation completed.
- Day 4: Document authorization, permissions, audit logging, admin activity, and bug fixes completed.
- Day 5: Deployment planned.
- Day 6: Security testing planned.
- Day 7: Final review and submission planned.

---

## Day 3 – Document Management (Completed)

### 1. Document Upload

- Implemented secure document upload using Flask.
- Added support for PDF, DOCX, TXT, PNG, JPG, and JPEG files.
- Added file extension validation.
- Added file size restrictions based on file type.
- Implemented secure filename handling.
- Generated unique stored filenames using UUID.
- Configured secure document storage inside the application instance folder.
- Added upload success and error messages.

### 2. Document Listing and Organization

- Implemented document listing functionality.
- Displayed uploaded document details.
- Added document category support.
- Implemented filename-based search.
- Added category-based filtering.
- Displayed upload timestamps in Indian Standard Time.
- Implemented document ordering by upload date.

### 3. Document Preview and Download

- Implemented document preview route.
- Implemented document download route.
- Added login and document access checks.
- Restricted unauthorized document access.

### 4. Document Categories

- Implemented General, Personal, Work, Education, and Finance categories.
- Added category selection during upload.
- Implemented category filtering.

**Status: Completed**

---

## Day 4 – Authorization and Audit Trail (Completed)

**Date: November 4, 2026**

### 1. Document Permission Management

- Created DocumentPermission database model.
- Implemented Read and Edit permission types.
- Added document sharing with registered users.
- Implemented permission granting through username.
- Added validation for sharing permissions.
- Prevented users from sharing their own documents with themselves.
- Implemented permission updates for existing shares.
- Implemented revoke document access functionality.
- Added permission ownership and authorization checks.

### 2. Document Access Control

- Implemented centralized document access checking.
- Added document owner and administrator access checks.
- Implemented shared document access for authorized users.
- Restricted unauthorized preview and download requests.
- Added Edit permission checks for document modifications.
- Restricted document deletion to owners and administrators.
- Implemented shared document visibility in the document listing.

### 3. Document Modification and Deletion

- Implemented document category editing route.
- Added authorization checks before modifying documents.
- Implemented document deletion route.
- Added authorization checks before deletion.
- Handled audit logging safely during document deletion.
- Deleted the database record before attempting physical file removal.

### 4. Audit Logging System

- Created AuditLog database model.
- Added actor, document, action, details, IP address, and timestamp fields.
- Implemented document upload activity logging.
- Implemented document preview activity logging.
- Implemented document download activity logging.
- Implemented permission grant activity logging.
- Implemented permission revocation activity logging.
- Implemented document modification activity logging.
- Implemented document deletion activity logging.
- Added audit tracking for important document operations.

### 5. Admin Activity Dashboard

- Implemented admin activity route.
- Added administrator role verification.
- Created the admin activity page at `templates/admin/activity.html`.
- Implemented display of recent audit activities.
- Restricted activity page access to administrators.
- Added admin activity link to the dashboard.

### 6. Bug Fixes and Verification

- Fixed category filtering issue.
- Fixed document deletion foreign-key constraint issue.
- Updated deletion audit logging to avoid foreign-key conflicts.
- Verified Python syntax for app.py, routes/documents.py, and models/audit_log.py using py_compile.

### 7. Security Test Verification - November 5, 2026

- Added pytest authentication and authorization coverage.
- Verified owner, viewer, and administrator access boundaries.
- Tested document sharing and permission revocation.
- Verified unauthorized preview and download requests return HTTP 403.
- Verified denied preview and download attempts generate audit records.
- Verified viewers cannot access the administrator activity page.
- Verified administrators can access the activity page.
- Full test suite result: **18 passed, 0 failed**.
- Identified 9 SQLAlchemy Query.get() deprecation warnings for future cleanup.

**Status: Completed**

---
## Day 5 - Deployment (Planned)

- Prepare the application for deployment.
- Configure production environment variables.
- Configure production database.
- Deploy the Flask application.
- Verify deployed application functionality.

## Day 6 – Security Testing (Planned)

- Test authentication and authorization.
- Test document access restrictions.
- Test permission granting and revocation.
- Test unauthorized access attempts.
- Test file upload validation.
- Review security threats and mitigations.
- Verify audit logging behavior.

## Day 7 – Final Review and Submission (Planned)

- Review project functionality.
- Verify documentation.
- Update README.md.
- Review PROMPTS.md and THREATS.md.
- Perform final testing.
- Prepare project demonstration and submission.

---

## Documentation

- PROMPTS.md: AI prompts, generated output, issues, and corrections.
- THREATS.md: Security threats, mitigations, and accepted risks.
- PROJECT_PLAN.md: Development plan and progress.
- README.md: Project setup and deployment instructions.

## Development Guidelines

- Implement mandatory requirements before optional enhancements.
- Verify AI-generated code before implementation.
- Document security issues honestly.
- Maintain documentation throughout development.
- Commit and push changes regularly.
- Test security controls before final submission.




## Day 5 – Deployment Preparation (November 5, 2026)

**Completed:**
- Added environment-variable configuration support for SECRET_KEY, DATABASE_URL, SESSION_COOKIE_SECURE, and DOCUMENT_STORAGE_PATH.
- Added a centralized configurable document storage path.
- Updated document upload, preview, download, and deletion routes to use the storage helper.
- Verified Python syntax.
- Ran the full test suite: 18 passed, 0 failed.
- Committed and pushed application changes to GitHub.

**Not completed:**
- Actual deployment and live application verification.
- Production SECRET_KEY enforcement.
- Production database setup and migration.
- Persistent storage configuration.
- Deployment entry-point verification.

**Carry forward to Day 6:**
Complete remaining security testing and production-readiness work, including CSRF, rate limiting, file signature validation, IDOR tests, and deployment preparation.

