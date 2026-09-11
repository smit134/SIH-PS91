# Authentication System Specification — Dhruv's Contribution

> **Current Status**: `Implemented`  
> *Note: Full JWT authentication, bcrypt password hashing, token lifecycles, and auth endpoints implemented in `app/core/security.py`, `app/core/deps.py`, and `app/api/v1/auth.py`. Verified via 10 automated tests.*

---

## 1. Authentication Architecture Overview

- **Design Objective**: Provide lightweight, robust, and secure authentication suitable for rural micro-entrepreneurs.
- **Protocol**: JSON Web Tokens (JWT) using Bearer authentication scheme over HTTP headers.
- **Key Identifiers**:
  - Primary: Phone Number (standard for Indian rural users).
  - Optional: Email address.
- **Password Security**: Cryptographic password hashing using `Argon2id` or `bcrypt` (work factor >= 12) with unique per-user salt. Plaintext passwords are never stored or logged.

---

## 2. Token & Session Lifecycle

- **Access Token**:
  - Format: JWT signed with `HS256` or `RS256` using application `SECRET_KEY`.
  - Lifetime: 60 minutes (`ACCESS_TOKEN_EXPIRE_MINUTES = 60`).
  - Claims:
    ```json
    {
      "sub": "<user_uuid>",
      "phone": "<phone_number>",
      "role": "ENTREPRENEUR",
      "type": "access",
      "exp": 1789000000,
      "iat": 1788996400
    }
    ```
- **Refresh Token (Planned)**:
  - Lifetime: 7 days.
  - Used at `/api/v1/auth/refresh` to obtain a new access token without re-entering credentials.
- **Logout / Session Termination**:
  - Client discards tokens.
  - Optional server-side token revocation / blocklist for enterprise security.

---

## 3. Endpoints Specification (From `project.md` Section 21.6)

### Registration (`POST /api/v1/auth/register`)
- **Input**: Phone number, password, full name, preferred language, role.
- **Process**:
  1. Validate phone number format and password complexity.
  2. Verify uniqueness of phone number in database.
  3. Hash password.
  4. Create user record and initialize empty capability profile.
- **Output**: HTTP `201 Created` with created user details (excluding password).

### Login (`POST /api/v1/auth/login`)
- **Input**: Credentials (phone/email + password).
- **Process**:
  1. Lookup user by identifier.
  2. Verify password against stored hash.
  3. Ensure account `is_active == True`.
  4. Generate access token and refresh token.
- **Output**: HTTP `200 OK` with `access_token`, `token_type: "bearer"`, and user profile summary.

### Refresh (`POST /api/v1/auth/refresh`)
- **Input**: Valid refresh token.
- **Output**: Newly minted access token.

### Request SMS OTP (`POST /api/v1/auth/otp/send`)
- **Input**: Mobile phone number (`+91XXXXXXXXXX`).
- **Protection**: Rate limited to 5 requests / 60 seconds.
- **Process**:
  1. Generates 6-digit cryptographic numeric code.
  2. Stores in-memory with 5-minute TTL and 3-attempt quota.
  3. Dispatches mock/gateway SMS.
- **Output**: HTTP `200 OK` with `expires_in_seconds: 300` and `is_registered_user` flag.

### Verify SMS OTP & Authenticate (`POST /api/v1/auth/otp/verify`)
- **Input**: Mobile phone, 6-digit `otp_code`, optional `full_name`, `language`.
- **Protection**: Rate limited to 10 requests / 60 seconds.
- **Process**:
  1. Verifies code and decrements attempt quota.
  2. If user exists: signs user in and returns tokens.
  3. If user does not exist: auto-registers user with `is_verified=True`, creates initial profile, logs `USER_REGISTER_OTP` audit event, and returns tokens.
- **Output**: HTTP `200 OK` with `TokenResponse` (access token, refresh token, user summary).

### Current User (`GET /api/v1/auth/me`)
- **Input**: `Authorization: Bearer <access_token>`.
- **Output**: Authenticated user's profile and active session state.


---

## 4. Authentication Dependencies (`deps.py`)

- **`oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")`**: Extracts Bearer token from header.
- **`get_current_user(token, db)`**:
  - Decodes token and verifies signature and expiration.
  - Fetches user from database via `sub` claim.
  - Raises `HTTPException(401)` if token is expired, invalid, or user does not exist.
- **`get_current_active_user(current_user)`**:
  - Ensures user account is not disabled/deactivated.

---

## 5. Protected Routes

Any endpoint requiring an authenticated user injects the dependency:

```python
@router.get("/profile")
async def get_profile(current_user: User = Depends(get_current_user)):
    ...
```

---

## 6. Failure Modes & Edge Cases

| Failure Scenario | HTTP Status | Response Code | Description |
| :--- | :--- | :--- | :--- |
| Missing `Authorization` header | `401 Unauthorized` | `UNAUTHORIZED` | Header missing or malformed |
| Expired JWT token | `401 Unauthorized` | `TOKEN_EXPIRED` | Token past expiration timestamp |
| Invalid signature / corrupt token | `401 Unauthorized` | `TOKEN_INVALID` | Signature validation failure |
| Incorrect phone or password | `401 Unauthorized` | `INVALID_CREDENTIALS` | Login credentials mismatch |
| Inactive / suspended account | `403 Forbidden` | `ACCOUNT_INACTIVE` | Account marked inactive by admin |
| Duplicate phone on registration | `409 Conflict` | `RESOURCE_CONFLICT` | Phone number already registered |

---

## 7. Verification & Implementation Notes
*(This section will be updated with actual test results and code references once implementation begins.)*
