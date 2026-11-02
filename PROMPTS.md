# AI Usage Log — SecureSpace

## Prompt 1: Project Analysis and Planning

### Prompt Given to AI

I am participating in the Snovasys Fresher Hiring Challenge 2026.

My project is SecureSpace, a secure document-sharing web application with a real audit trail.

I am a beginner in Python and web development. I know basic HTML and CSS. I plan to use Python Flask, SQLite, HTML, CSS, and JavaScript.

Please analyze the project requirements in detail and explain:

1. The main features I need to implement.
2. The user roles and permissions.
3. The security requirements and possible threats.
4. The database tables I may need.
5. The project architecture and folder structure.
6. A step-by-step development plan suitable for a beginner.
7. Which features are mandatory for the hackathon.
8. How I can maximize the evaluation score.

Explain everything in simple language.

### AI Response Summary

The AI analyzed the project requirements and suggested a secure document-sharing architecture with authentication, role-based access control, document management, permission management, audit logging, search, and security testing.

### My Review

I reviewed the AI suggestions and compared them with the official hackathon requirements.

I decided to use Python Flask, SQLite, HTML, CSS, and JavaScript as the technology stack.

I also decided to prioritize mandatory requirements and security features before implementing optional enhancements.

### Final Decision

I will build SecureSpace step by step, following a 7-day development plan.

I will verify AI-generated suggestions against the official project requirements and correct any mistakes before implementing them.

## Day 2 - Authentication and Security

### Entry 1 - User Registration
Date: 2026-11-02

Prompt:
Help me implement user registration in SecureSpace using Flask and SQLite. Check the existing project structure and use the existing User model.

AI Output:
Generated registration logic with username, email, password hashing, and database insertion.

Issue:
The initial implementation did not validate all inputs and did not check for duplicate email addresses.

Correction:
Added input validation and duplicate username/email checks.

Commit:
Pending

### Entry 2 - User Login
Date: 2026-11-02

Prompt:
Help me implement login functionality using Flask-Login. Users should log in with their registered username and password.

AI Output:
Generated login logic using password hash verification.

Issue:
The initial implementation did not include login attempt rate limiting.

Correction:
Rate limiting is not implemented yet. This remains a security risk to address.

Commit:
Pending

### Entry 3 - Dashboard Access Control
Date: 2026-11-02

Prompt:
Help me protect the SecureSpace dashboard so only authenticated users can access it.

AI Output:
Generated a dashboard route using Flask-Login login_required.

Issue:
Authentication protects the dashboard, but it does not enforce document-level permissions or role-based authorization.

Correction:
Document-level authorization is planned for the document sharing implementation.

Commit:
Pending

### Entry 4 - Authentication Security Review
Date: 2026-11-02

Prompt:
Review the login and registration code for security issues. Check whether authentication is sufficient to protect user resources.

AI Output:
Identified password hashing and authentication checks.

Issue:
The review did not implement authorization checks for individual documents.

Correction:
Document ownership and permission checks must be implemented before document access features are considered secure.

Commit:
Pending

### Entry 5 - Session and Logout
Date: 2026-11-02

Prompt:
Help me implement logout using Flask-Login and check whether the logout route is protected.

AI Output:
Generated a logout route.

Issue:
Logout was initially implemented using GET, which is not ideal for a state-changing operation.

Correction:
Changed logout to POST. CSRF protection still needs to be verified.

Commit:
Pending

## Reusable Context

- PROBLEM_STATEMENT.md: Mandatory project requirements.
- THREATS.md: Security threat analysis and mitigation tracking.
- AI_TOOLS.md: AI usage instructions.
- PROMPTS.md: Development prompts and AI output review.

