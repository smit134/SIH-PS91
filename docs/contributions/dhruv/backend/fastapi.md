# FastAPI Backend Architecture — Dhruv's Contribution

> **Current Status**: `Partially Implemented`  
> - **Foundation, Config, Lifecycle & Error Envelopes**: `Implemented`  
> - **Domain Routers & DB Integration**: `Planned`  
> *Note: Application factory, CORS, exception handlers, health checks, and test suite are implemented and verified.*

---

## 1. Application Structure

The proposed layout strictly isolates concerns while exposing clean entry points for team members:

```text
backend/
├── app/
│   ├── main.py                     # FastAPI application factory, CORS, global middlewares
│   ├── config.py                   # Pydantic BaseSettings (env configs, DB URI, JWT keys)
│   ├── core/
│   │   ├── database.py             # Async SQLAlchemy engine & session maker
│   │   ├── security.py             # Password hashing routines, JWT encoding/decoding
│   │   ├── deps.py                 # Common FastAPI dependencies (get_db, get_current_user)
│   │   └── exceptions.py           # Custom exception classes and global handlers
│   ├── models/                     # SQLAlchemy 2.0 ORM models
│   ├── schemas/                    # Pydantic DTOs for request/response serialization
│   ├── api/                        # Domain-driven router structure
│   │   └── v1/
│   │       ├── api.py              # Root v1 router aggregating all endpoints
│   │       ├── auth.py             # Auth endpoints (Owned by Dhruv)
│   │       ├── profile.py          # Entrepreneur profile endpoints (Owned by Dhruv)
│   │       ├── businesses.py       # Opportunities router (Integration point for Aishwarya)
│   │       ├── partners.py         # Partner matching router (Integration point for Aishwarya)
│   │       ├── finance.py          # Financial simulator router (Integration point for Kesha)
│   │       ├── schemes.py          # Scheme routing router (Integration point for Kesha)
│   │       └── evidence.py         # Evidence retrieval router (Integration point for Smit)
│   └── seed/                       # Database seed scripts for testing and demo
```

---

## 2. Application Startup & Lifespan

- **Framework**: FastAPI (async ASGI application).
- **Lifespan Context Manager**:
  - `startup`: Initialize async database connection pool, verify PostGIS extension availability, load initial application settings.
  - `shutdown`: Gracefully close database connection pools and clean up active sessions.

---

## 3. Configuration & Environment Variables

- Managed via Pydantic `BaseSettings` reading from `.env`:
  - `PROJECT_NAME`: ThinkForge API
  - `API_V1_STR`: `/api/v1`
  - `DATABASE_URL`: `postgresql+asyncpg://<user>:<pass>@<host>:<port>/<dbname>`
  - `SECRET_KEY`: Cryptographic key for JWT token signing
  - `ALGORITHM`: `HS256`
  - `ACCESS_TOKEN_EXPIRE_MINUTES`: 60
  - `REFRESH_TOKEN_EXPIRE_DAYS`: 7
  - `CORS_ORIGINS`: Allowed origins (e.g., `http://localhost:3000`)

---

## 4. Routers & Services

- Routers receive requests, invoke FastAPI dependencies for validation and authentication, and call domain services.
- Dhruv provides the core routing infrastructure (`/auth`, `/profile`, base health check) and provides mounting points for domain routers developed by teammates.

---

## 5. Schemas (Pydantic DTOs)

- All request payloads and response bodies are strictly validated using Pydantic V2 models.
- Response models utilize `from_attributes = True` for direct ORM-to-JSON serialization.
- Schemas strictly separate internal database fields (like `hashed_password`) from external representations.

---

## 6. Dependency Injection (`deps.py`)

- `get_db()`: Yields an async SQLAlchemy `AsyncSession` with transactional safety and auto-rollback on uncaught exceptions.
- `get_current_user()`: Decodes Bearer JWT token, validates user existence in DB, and enforces active status.
- `get_current_active_user()`: Validates that the authenticated user account is active.
- `require_role(role)`: RBAC enforcement dependency.

---

## 7. Middleware

- **CORS Middleware**: Explicit origin, method, and header whitelisting for Next.js frontend clients.
- **Request ID & Logging Middleware**: Attaches a unique UUID to each incoming request for end-to-end tracing in logs.
- **Security Headers Middleware**: Enforces standard security headers (`X-Content-Type-Options`, `X-Frame-Options`, `Content-Security-Policy`).

---

## 8. Exception Handling & Logging

- Global exception handlers catching:
  - `RequestValidationError`: Formats Pydantic validation failures into standardized 422 JSON errors.
  - `HTTPException`: Uniform API error response envelope.
  - `SQLAlchemyError`: Database exception sanitization (prevents exposing internal DB structure).
  - Unhandled exceptions: Returns a clean 500 error and logs stack traces internally.
- Structured logging using Python `logging` with ISO-8601 timestamps and request IDs.

---

## 9. Request Lifecycle

1. Client sends HTTP request.
2. ASGI server (Uvicorn) passes request to FastAPI pipeline.
3. Middlewares attach request ID and process CORS.
4. Route resolution matching `/api/v1/...`.
5. Dependency injection resolves `AsyncSession` and authenticated user.
6. Request payload validated against Pydantic schema.
7. Service layer executes business logic and database queries.
8. Response serialized to standard JSON response schema.
9. Database session closed/committed.
10. HTTP response returned to client.

---

## 10. Database Interaction

- Async interactions through `asyncpg` and SQLAlchemy 2.0.
- No blocking synchronous queries inside async route handlers.
- Transactions are scoped per request.

---

## 11. Authentication Interaction

- Routes needing authentication declare `current_user: User = Depends(get_current_user)`.
- Anonymous routes (such as `/auth/login`, `/auth/register`, `/health`) omit the user dependency.

---

## 12. Verification & Updates
*This section will be populated with actual code references and verification logs once implementation begins.*
