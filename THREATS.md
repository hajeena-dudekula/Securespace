# SecureSpace – Security Threat Analysis

## 1. Project Information

- **Project:** SecureSpace – Secure Document Sharing with a Real Audit Trail
- **Challenge:** Snovasys Fresher Hiring Challenge 2026
- **Application:** Flask-based document-sharing application
- **Database:** SQLite (current development configuration)
- **Review date:** 2026-11-09

## 2. Purpose

This document identifies security threats affecting SecureSpace, describes the controls implemented to mitigate them, and records the remaining limitations.

The security objective is to prevent unauthorized users from accessing confidential documents and maintain an accountable record of document activities.

A security control is not considered fully verified merely because its code exists. Relevant tests and deployment checks are also required.

## 3. Threat Register

### Threat 1 – Unauthorized Document Access

**Risk:** A user may attempt to access another user's document by changing a document ID or directly requesting a preview or download URL.

**Implemented controls:**
- Login is required for protected document operations.
- Document ownership and sharing permissions are checked on the server.
- Preview and download routes perform document-level access checks.
- Stored filenames use UUID-based identifiers.
- Private document storage is used instead of exposing uploaded files through public static routes.

**Verification:**
- Cross-user document access scenarios are covered by authorization tests.
- Unauthorized preview and download attempts are tested.
- Denied access attempts generate security audit events.

**Remaining limitations:**
- Live production access-control behavior still requires deployment verification.
- Additional testing with production database and storage configuration is required.

**Status:** Core authorization and cross-user tests implemented.

### Threat 2 – Broken Access Control and Privilege Escalation

**Risk:** A viewer or editor may attempt operations beyond their assigned permissions.

**Implemented controls:**
- Read and Edit permissions are supported.
- Document modifications require appropriate edit access.
- Sharing and revocation are restricted to document owners.
- Document deletion is restricted to owners and administrators.
- Administrator activity access is restricted by role.
- Permission Advisor suggestions do not automatically grant permissions.

**Verification:**
- Owner, viewer, editor, and administrator access boundaries have test coverage.
- Unauthorized sharing, revocation, editing, and deletion attempts are covered.
- Permission Advisor authorization tests verify that unauthorized users cannot request suggestions for another owner's document.

**Remaining limitations:**
- Continue reviewing every new document-related endpoint whenever functionality changes.

**Status:** Core authorization controls implemented and tested.

### Threat 3 – Malicious or Invalid File Uploads

**Risk:** An attacker may upload unsupported, oversized, malformed, or potentially harmful files.

**Implemented controls:**
- Allowed extensions are restricted to supported document and image formats.
- File-size restrictions are configured.
- Secure filename handling is used.
- UUID-based stored filenames reduce filename collision and path manipulation risks.
- File content signature checks are implemented for supported formats.
- Uploaded files are stored in private storage.
- Upload security tests are included.

**Remaining limitations:**
- File signature validation is not a complete malware detection mechanism.
- No malware scanning service is currently integrated.
- Malformed-file and advanced content-based attacks require additional testing.

**Status:** Basic upload restrictions, signature validation, and security tests implemented.

### Threat 4 – Audit Log Modification or Deletion

**Risk:** An attacker may modify or delete audit records to hide document activity.

**Implemented controls:**
- Audit records contain actor, document reference, action, details, IP address, and timestamp.
- Important document operations create audit events.
- Denied access attempts are recorded.
- Audit records are linked using HMAC-based SHA-256 integrity hashes.
- A verification function checks the audit chain.
- Existing audit records were backfilled with integrity hashes.
- Audit integrity tests are included.

**Remaining limitations:**
- Audit records currently use application database storage.
- External immutable or append-only audit storage is not configured.
- Deletion of the final audit record may not be detected by an internal chain alone.
- An attacker controlling both the database and signing secret may be able to reconstruct the chain.
- The audit signing secret must remain stable; changing it without a planned migration will invalidate existing verification.

**Status:** Tamper-evident audit chain implemented and tested. External tamper-resistant storage remains pending.

### Threat 5 – Permission Revocation Failure

**Risk:** A previously authorized user may retain access after the owner revokes permission.

**Implemented controls:**
- Owners can revoke document permissions.
- Access checks use current permission records.
- Preview and download requests perform authorization checks rather than relying only on an earlier session decision.

**Verification:**
- Revoked-user access behavior is covered by permission tests.
- Subsequent unauthorized document operations are expected to be denied.

**Remaining limitations:**
- Production database and multi-worker behavior require live verification.

**Status:** Revocation functionality and authorization tests implemented.

### Threat 6 – Session Hijacking and CSRF

**Risk:** An attacker may misuse an exposed authenticated session or trick a logged-in user into submitting an unwanted state-changing request.

**Implemented controls:**
- Flask-Login manages authentication sessions.
- Logout uses POST.
- Flask-WTF CSRF protection is configured.
- CSRF tokens are included in relevant POST forms.
- HTTP-only session cookies are enabled.
- SameSite=Lax is configured.
- Secure cookies are enabled in production configuration.

**Verification:**
- CSRF rejection has a dedicated test.
- Authentication and logout behavior are covered by tests.

**Remaining limitations:**
- HTTPS and secure cookie behavior must be verified on the actual production deployment.
- Session security requires review whenever new state-changing routes or forms are introduced.

**Status:** Core session and CSRF protections implemented; production verification pending.

### Threat 7 – SQL Injection

**Risk:** Malicious input may attempt to manipulate database queries.

**Implemented controls:**
- SQLAlchemy ORM is used for database operations.
- Document search and filtering use ORM query construction.

**Remaining limitations:**
- Dedicated SQL injection testing should be performed against relevant input paths.
- Any future raw SQL must use parameterized queries.

**Status:** ORM-based database access implemented; dedicated injection testing remains a review item.

### Threat 8 – Brute-Force Login Attempts

**Risk:** An attacker may repeatedly guess account passwords.

**Implemented controls:**
- Werkzeug password hashing is used.
- Flask-Limiter is configured for login rate limiting.
- The login POST endpoint has a limit of five attempts per minute.
- A rate-limit test verifies that excessive login attempts are rejected.

**Remaining limitations:**
- Production requires an accessible Redis service for shared rate-limit storage.
- A Render Redis service has been provisioned. Application connectivity and shared rate-limit behavior require production verification.

**Status:** Login rate limiting implemented and tested; production Redis infrastructure provisioned, with application connectivity verification remaining.

### Threat 9 – Weak Password Storage

**Risk:** Plain-text password storage could expose user passwords if the database is compromised.

**Implemented controls:**
- Werkzeug password hashing is used.
- Password verification uses stored password hashes.
- Registration does not store submitted passwords as plain text.
- Default registration assigns the viewer role.

**Remaining limitations:**
- Continue checking password-handling changes during future reviews.

**Status:** Password hashing implemented.

### Threat 10 – Insecure Production Configuration

**Risk:** Development secrets, insecure cookies, temporary storage, or incorrect application startup configuration may expose the application.

**Implemented controls:**
- Environment-based configuration is supported.
- Production requires SECRET_KEY and AUDIT_LOG_SECRET.
- Production secret values must meet the configured minimum length.
- Production session cookies are configured as secure.
- Production rate limiting rejects the memory-only backend.
- Configurable document storage paths are supported.
- The deployment entrypoint loads the root application implementation.
- Gunicorn and Redis dependencies are listed in requirements.txt.

**Remaining limitations:**
- A new Render web service has been created and configured for deployment.
- A Render PostgreSQL database has been provisioned; application connectivity and production data migration require verification.
- Persistent private file storage must be configured and tested.
- A Render Redis service has been provisioned; application connectivity requires verification.
- HTTPS and live deployment behavior must be verified.
- Production secrets must be stored securely outside the repository.

**Status:** Production configuration safeguards implemented; actual deployment remains pending.

## 4. Security Testing Coverage

The current automated test suite includes coverage for:

1. Authentication and protected routes.
2. Document ownership and cross-user access restrictions.
3. Viewer, editor, owner, and administrator permissions.
4. Sharing and revocation behavior.
5. Unauthorized preview and download attempts.
6. Denied-access audit events.
7. Upload security and file validation.
8. Audit-chain integrity verification.
9. Document owner and date filters.
10. Permission Advisor recommendations and authorization.
11. Login rate limiting.
12. CSRF protection.

**Latest full test result (2026-11-09):**

- Passed: 78
- Failed: 0
- Warnings: 1

The single warning relates to Flask-Login using the deprecated datetime.utcnow() method. It is not a test failure.

Passing automated tests do not establish that every possible attack has been prevented. Production testing and additional security review remain necessary.

## 5. Current Security Status

| Security area | Current status |
|---|---|
| Password hashing | Implemented |
| User authentication | Implemented |
| Role-based access checks | Implemented and tested |
| Document ownership checks | Implemented and tested |
| Read/Edit permissions | Implemented and tested |
| Share and revoke operations | Implemented and tested |
| Unauthorized access logging | Implemented and tested |
| Private document storage | Implemented |
| File extension and size restrictions | Implemented |
| File signature validation | Implemented and tested |
| Path traversal protection | Implemented and tested |
| Login rate limiting | Implemented and tested |
| CSRF protection | Implemented and tested |
| HMAC audit integrity chain | Implemented and tested |
| Document search and filters | Implemented and tested |
| Permission Advisor | Implemented; owner approval required |
| SQL injection review | ORM used; dedicated testing pending |
| Malware scanning | Not implemented |
| External immutable audit storage | Not implemented |
| Production secret validation | Implemented |
| Production Redis service | Provisioned; connectivity verification required |
| Production database | Provisioned; connectivity verification required |
| Live HTTPS deployment verification | Requires final operational verification |

## 6. Accepted Security Gaps and Limitations

- File signature checks cannot guarantee that an uploaded file is harmless.
- Malware scanning is not currently integrated.
- The HMAC audit chain is tamper-evident, not completely tamper-proof.
- Database-backed audit records do not provide the same guarantees as independent immutable storage.
- Audit signing secrets must be protected and kept consistent with existing records.
- The in-memory rate-limit backend is suitable only for development; production requires Redis.
- Production security settings have not yet been verified on a live deployment.
- Automated tests cover identified scenarios but cannot prove the absence of all vulnerabilities.

## 7. Review History

### Day 1 – Initial Threat Identification

Identified unauthorized document access, broken access control, malicious uploads, audit modification, permission revocation failure, session misuse, and SQL injection as important risks.

### Day 2 – Authentication Security

Implemented registration, login, password hashing, authenticated dashboard access, and POST-based logout.

### Day 3 – Document Management

Implemented document upload, listing, search, preview, download, category handling, and basic file restrictions.

### Day 4 – Authorization and Audit Trail

Implemented document-level permissions, sharing, revocation, owner and administrator checks, and activity logging.

### Day 5 – Deployment Preparation (November 5, 2026)

- Added environment-based application configuration.
- Added configurable private document storage path handling.
- Updated upload, preview, download, and deletion operations to use the storage helper.
- Verified application syntax and existing tests.
- Actual production deployment remained pending.

### Day 6 – Security Hardening (November 6, 2026)

- Added login rate limiting and tests.
- Added CSRF protection and rejection testing.
- Added file signature validation and upload security tests.
- Added document owner and date filters.
- Added HMAC-based audit-chain integrity verification.
- Added Permission Advisor with mandatory owner approval.
- Added production secret validation.
- Updated the application entrypoint.
- Added production Redis enforcement.
- Historical test result at that review: 52 passed, 0 failed. This was superseded by the latest full test result: 78 passed, 0 failed.

### Next Review

Production validation areas: Redis connectivity, database connectivity and migration, persistent storage, live HTTPS behavior, malware-scanning evaluation, and external audit-storage evaluation.
