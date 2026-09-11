# Security & Privacy Controls — Dhruv's Contribution

> **Current Status**: `Planned / Not Yet Implemented`  
> *Note: In accordance with safety rules, no security control is claimed as implemented until it has been written, tested, and verified.*

---

## 1. Security Controls Classification Matrix

| Security Domain | Control | Implemented | Planned | Future |
| :--- | :--- | :---: | :---: | :---: |
| **Input Validation** | Strict Pydantic V2 schema validation on all endpoints | ✅ | | |
| **Input Validation** | Phone number E.164 sanitization & regex constraints | ✅ | | |
| **Authentication** | Cryptographic password hashing (bcrypt >= 12 rounds) | ✅ | | |
| **Authentication** | Short-lived JWT access tokens (60 min expiration) | ✅ | | |
| **Authentication** | Cryptographic signature verification with PyJWT HS256 | ✅ | | |
| **Authentication** | Dual-token access & refresh lifecycle (`/auth/refresh`) | ✅ | | |
| **Authentication** | Token revocation / blacklisting mechanism | ❌ | | ✅ |
| **Authentication** | Multi-factor / OTP verification provider integration | ❌ | | ✅ |
| **Authorization** | Strict user ownership verification on all resource routes | ❌ | ✅ | |
| **Authorization** | Role-based access control (`require_role`: ENTREPRENEUR, ADVISOR, ADMIN) | ✅ | | |
| **Secret Management** | Pydantic BaseSettings loading from isolated `.env` | ✅ | | |
| **Secret Management** | Automated secret rotation & HashiCorp Vault / Cloud KMS | ❌ | | ✅ |
| **CORS Policy** | Whitelist-only CORS middleware restricted to Next.js frontend | ✅ | | |
| **Rate Limiting** | Endpoint rate limiting on login/register routes (e.g. SlowAPI) | ❌ | ✅ | |
| **API Security** | Standard error envelope masking internal server tracebacks | ✅ | | |
| **API Security** | Request size limiting to prevent payload-based DoS | ❌ | ✅ | |
| **Database Security** | Parameterized queries via SQLAlchemy (SQL injection prevention) | ✅ | | |
| **Database Security** | Dedicated non-superuser database credentials for application | ❌ | ✅ | |
| **Privacy Controls** | Location fuzzing / coordinate obfuscation for public cards | ❌ | ✅ | |
| **Privacy Controls** | Mutual-consent gate before contact data exchange (Section 33) | ❌ | ✅ | |
| **Privacy Controls** | Masking exact individual bank balances | ❌ | ✅ | |
| **Audit & Logging** | Audit log table tracking critical auth and consent events | ✅ | | |
| **Audit & Logging** | PII and credential masking in all server log streams | ✅ | | |

---

## 2. Details of Implemented Controls

*None currently.* Implementation has not yet commenced.

---

## 3. Details of Planned Controls

### Input Validation
- All inputs are parsed by Pydantic models with type checking, length constraints, and regex patterns (e.g., regex pattern `^\+91[6-9]\d{9}$` for Indian mobile numbers).
- Payloads containing unexpected or malicious keys are rejected by strict schema validation.

### Password Security & Hashing
- Password hashing using `PassLib` with `Argon2id` or `bcrypt`.
- Plaintext passwords exist only in memory during the duration of the hashing function and are never written to disk, database, or logs.

### Secret Management
- Secrets (`SECRET_KEY`, `DATABASE_URL`) are read from environment variables or a local `.env` file that is strictly excluded from version control via `.gitignore`.
- Development defaults will fail loudly in production if default dummy keys are detected.

### CORS & Transport Security
- Allowed CORS origins are restricted to `http://localhost:3000` during local development, and production domain in deployment. Wildcard `*` origins are strictly prohibited.

### Privacy Controls (Section 33 Compliance)
- **Fuzzy Geolocation**: Exact GPS coordinates are never returned in public partner searches. The API transforms points to approximate center coordinates or distance bands (e.g., "within 7 km").
- **Mutual Consent**: A database-enforced relationship table (`partner_matches`) tracks consent states (`PENDING`, `ACCEPTED`, `REJECTED`). Contact information is conditionally serialized only when status is `ACCEPTED`.

---

## 4. Future Security Hardening
- Hardware security key / WebAuthn support.
- Centralized SIEM integration and automated anomaly detection for brute-force attacks.
