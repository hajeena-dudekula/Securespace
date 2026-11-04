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

**Tasks:**

- Implemented secure document upload using Flask.
- Added file extension validation.
- Added file size restrictions based on file type.
- Generated unique filenames using UUID.
- Stored uploaded documents securely.
- Implemented document listing.
- Organized documents using categories.
- Implemented filename-based document search.
- Implemented category-based filtering.
- Implemented document preview.
- Implemented document download.
- Added support for PDF, DOCX, TXT, PNG, JPG, and JPEG files.
- Implemented General, Personal, Work, Education, and Finance categories.
- Added category selection during document upload.

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
- Added document owner access.
- Added administrator access checks.
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
- Created admin activity page.
- Implemented display of recent audit activities.
- Restricted activity page access to administrators.
- Added admin activity link to the dashboard.

### 6. Bug Fixes and Verification

- Fixed category filtering issue.
- Fixed document deletion foreign-key constraint issue.
- Implemented safe audit logging for document deletion.
- Verified Python syntax using py_compile.

**Status: Completed**

---
## Day 5 – Deployment (Planned)

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

