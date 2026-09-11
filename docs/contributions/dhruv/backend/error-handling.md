# Error Handling Standards — ThinkForge Backend

> **Current Status**: `Implemented`  
> *Note: Exception classes and global handlers are implemented in `app/core/exceptions.py` and verified via pytest.*

---

## 1. Error Categories & Handling Rules

### Validation Errors (`422 Unprocessable Entity`)
- **Origin**: Pydantic model validation on incoming request JSON bodies, query parameters, path variables, or headers.
- **Handling**: Caught by a custom `RequestValidationError` handler in `main.py`.
- **Response**: Sanitized list of error locations and human-readable error messages. No stack traces exposed.

### Authentication Errors (`401 Unauthorized`)
- **Origin**: Missing `Authorization` header, invalid JWT signature, expired token, unsupported token type, or nonexistent user subject.
- **Handling**: Raised explicitly as `HTTPException(status_code=401, detail="...", headers={"WWW-Authenticate": "Bearer"})`.
- **Response**: Standardized error envelope explaining the authentication failure.

### Authorization Errors (`403 Forbidden`)
- **Origin**: User authenticated successfully, but does not own the requested resource (e.g., attempting to read another user's private financial data or profile without consent) or lacks the required role (e.g., non-admin accessing system endpoints).
- **Handling**: Raised by dependency guards (`require_ownership`, `require_role`).
- **Response**: `403 Forbidden` with a message that the action is not permitted.

### Database Errors (`409 Conflict` / `500 Internal Server Error`)
- **Origin**: Unique constraint violations (e.g., phone number already exists), foreign key constraint violations, query timeouts, or connection failures.
- **Handling**:
  - `IntegrityError` (Unique violation): Caught in the repository/service layer and converted to `409 Conflict` with a clean message (e.g., "A user with this phone number already exists.").
  - Connection/Operational errors: Caught globally, logged with full stack trace, and returned as a generic `500 Internal Server Error` to the client. Internal table or database names are never exposed.

### Not Found Errors (`404 Not Found`)
- **Origin**: Requested entity ID does not exist in the database or does not belong to the user's tenant.
- **Handling**: Raised as `HTTPException(status_code=404, detail="<Resource> not found")`.
- **Response**: Uniform 404 error envelope.

### Unexpected Errors (`500 Internal Server Error`)
- **Origin**: Uncaught runtime exceptions, syntax issues, unhandled Third-Party API timeouts.
- **Handling**: Caught by global exception middleware `catch_unhandled_exceptions`.
- **Response**: Generic error message: "An unexpected error occurred. Please try again later."
- **Internal Action**: Triggers an `ERROR` level log with full traceback and request ID.

---

## 2. API Error Response Envelope

All API errors return a standard JSON payload:

```json
{
  "error": {
    "code": "STRING_IDENTIFIER",
    "message": "Human-readable description of the error.",
    "details": null,
    "timestamp": "2026-09-10T12:00:00Z"
  }
}
```

### Standard Error Code Registry

| Error Code | HTTP Status | Description |
| :--- | :--- | :--- |
| `VALIDATION_ERROR` | 422 | Request body or parameter validation failed |
| `INVALID_CREDENTIALS` | 401 | Phone/email or password incorrect |
| `TOKEN_EXPIRED` | 401 | JWT access token has expired |
| `TOKEN_INVALID` | 401 | Malformed or untrusted token |
| `FORBIDDEN_RESOURCE` | 403 | Insufficient permissions or ownership violation |
| `RESOURCE_NOT_FOUND` | 404 | Target entity does not exist |
| `RESOURCE_CONFLICT` | 409 | Duplicate entity or state conflict |
| `DATABASE_ERROR` | 500 | Database connectivity or internal query failure |
| `INTERNAL_ERROR` | 500 | Unhandled application exception |

---

## 3. Logging Expectations

- **Log Level Standards**:
  - `DEBUG`: Query timing, raw parameters (with sensitive data masked).
  - `INFO`: Lifecycle events (startup, shutdown), successful logins, route dispatch.
  - `WARNING`: Failed login attempts, 404 occurrences, token validation rejections.
  - `ERROR`: 500 errors, database connection drops, external service failures.
  - `CRITICAL`: System-wide failure preventing application startup.
- **Contextual Logging**:
  - Every log entry must include:
    - ISO-8601 Timestamp
    - Log Level
    - Request ID (`X-Request-ID`)
    - Module name
    - Message
- **Sensitive Data Masking**:
  - Passwords, JWT secrets, authentication tokens, and Aadhaar/PII must NEVER be logged to stdout or files.
