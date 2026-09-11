# Scoped Requirements — Dhruv's Contribution

## 1. Backend Core & Foundation (BC)
- **REQ-BC-01**: Async FastAPI application factory with modular router mounting under `/api/v1`.
- **REQ-BC-02**: Pydantic BaseSettings loading configuration from environment variables / `.env`.
- **REQ-BC-03**: Strict CORS middleware restricted to frontend client origins.
- **REQ-BC-04**: Global exception handlers producing standardized JSON error envelopes (`{ "error": { "code", "message", "details", "timestamp" } }`).
- **REQ-BC-05**: Health check endpoint `GET /health` reporting application and database readiness.

## 2. Database & Spatial Layer (DB)
- **REQ-DB-01**: Async SQLAlchemy 2.0 engine and session factory with connection pooling and auto-rollback on uncaught exceptions.
- **REQ-DB-02**: Dependency `get_db` yielding request-scoped async database sessions.
- **REQ-DB-03**: PostgreSQL 16 schema models:
  - `User`: UUID primary key, phone (unique), hashed password, role, is_active.
  - `Profile`: User ID (FK), full name, location_geom (PostGIS Point), language, capital, risk tolerance.
  - `Skill` & `UserSkill`: Normalized skill catalog and user mapping with proficiency level.
  - `Resource` & `UserResource`: Physical asset inventory (land, machinery, vehicle, storage).
  - `BusinessCategory`: Benchmarked business models with capital and operating bounds.
  - `PartnerProfile` & `PartnerMatch`: Investment range, synergy score, mutual-consent status.
  - `EvidenceRecord`: Hyper-local data with source and reliability class (`VERIFIED`, `DERIVED`, `ESTIMATED`, `UNKNOWN`).
  - `AuditLog`: Security and data access trail.
- **REQ-DB-04**: GIST spatial indexes on geometry columns to support radius queries (`ST_DWithin`).
- **REQ-DB-05**: Alembic migration setup with async environment and linear revision tracking.

## 3. Authentication & Security (AUTH)
- **REQ-AUTH-01**: Cryptographic password hashing using Argon2id or bcrypt (work factor >= 12).
- **REQ-AUTH-02**: JWT Access Token issuance with 60-minute expiration.
- **REQ-AUTH-03**: Registration endpoint `POST /api/v1/auth/register` supporting phone number + password + role.
- **REQ-AUTH-04**: Login endpoint `POST /api/v1/auth/login` validating credentials and returning access token.
- **REQ-AUTH-05**: Dependency `get_current_user` validating Bearer JWT and loading active user from database.
- **REQ-AUTH-06**: Privacy safeguards:
  - Coordinate obfuscation for public partner discovery endpoints.
  - Mutual-consent enforcement: partner contact details hidden until mutual interest confirmed.
  - Plaintext passwords and tokens never written to logs.

## 4. Team Integration Contracts (INT)
- **REQ-INT-01**: OpenAPI / Swagger UI generated at `/docs` with request/response schemas.
- **REQ-INT-02**: Router mount and Pydantic schemas for `/businesses` (Aishwarya's Opportunity Engine).
- **REQ-INT-03**: Router mount and Pydantic schemas for `/partners` (Aishwarya's Partner Engine).
- **REQ-INT-04**: Router mount and Pydantic schemas for `/finance` (Kesha's Financial Engine).
- **REQ-INT-05**: Router mount and Pydantic schemas for `/schemes` (Kesha's Scheme Engine).
- **REQ-INT-06**: Router mount and Pydantic schemas for `/evidence` (Smit's RAG / Data Pipeline).
