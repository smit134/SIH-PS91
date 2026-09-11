# Architectural Decision Records (ADRs) — Dhruv's Scope

This document maintains the record of architectural decisions made during the design and implementation of Dhruv's assigned scope (Backend Core, Database & Auth Logic).

---

## ADR Template

When an architectural or engineering decision is reached, append a new entry using this exact format:

```markdown
## Decision: [Descriptive Decision Name]

- **Date**: YYYY-MM-DD
- **Status**: [Proposed | Accepted | Superseded | Deprecated]

### Context
Background context and state of the application leading up to this decision.

### Problem
The specific technical, architectural, or organizational challenge that required a decision.

### Alternatives
- **Option 1**: Description, pros, and cons.
- **Option 2**: Description, pros, and cons.

### Chosen Approach
Clear statement of the selected alternative.

### Reason
Why this option was selected over the alternatives (trade-offs, constraints, requirements).

### Consequences
- **Positive**: Expected benefits and improvements.
- **Negative / Risks**: Downsides, added complexity, or maintenance overhead.

### Related Implementation
File paths or modules directly impacted by this decision.

### Related Commit
Git commit hash where this decision was implemented in code.
```

---

## Logged Architectural Decisions

## Decision: ADR-001 — Centralized RFC-Compliant Error Envelope and FastAPI Application Factory

- **Date**: 2026-09-10
- **Status**: Accepted

### Context
ThinkForge integrates multiple distinct submodules developed by six different team members, consumed by a Next.js frontend. Without a standardized error envelope and application factory, error responses would vary across endpoints (e.g., standard FastAPI 422 lists vs raw 500 strings), complicating frontend UI state handling and error boundary displays.

### Problem
How should the backend structure its application lifecycle and guarantee uniform error responses across all endpoints and exception types?

### Alternatives
- **Option 1**: Rely on default FastAPI exception handlers and manually format errors in each route.
  - *Pros*: Low upfront setup.
  - *Cons*: Highly inconsistent, error-prone, violates DRY, and risks leaking internal database traces.
- **Option 2**: Global exception handlers registered via an application factory producing a standardized `{ "error": { "code", "message", "details", "timestamp" } }` schema.
  - *Pros*: Completely uniform, testable, masks sensitive server internals, conforms to API conventions.
  - *Cons*: Requires custom handler registration for `RequestValidationError` and `StarletteHTTPException`.

### Chosen Approach
Option 2: Implement an application factory (`create_application()`) in `app/main.py` with custom exception handlers in `app/core/exceptions.py`.

### Reason
Provides strict predictability for Madhav and Harshanshu's frontend data fetching layers while simplifying automated testing via `httpx.AsyncClient`.

### Consequences
- **Positive**: Consistent error payloads across 400, 401, 403, 404, 409, 422, and 500 status codes. Prevents internal traceback leakage to end users.
- **Negative**: All custom domain exceptions must inherit from `APIException` to maintain uniform code structure.

### Related Implementation
- `backend/app/main.py`
- `backend/app/core/exceptions.py`
- `backend/app/schemas/common.py`
- `backend/tests/test_exceptions.py`

### Related Commit
Pending initial backend commit.

---

## Decision: ADR-002 — Cross-Dialect UUID Primary Keys and Lazy Engine Initialization

- **Date**: 2026-09-11
- **Status**: Accepted

### Context
ThinkForge utilizes PostgreSQL 16 with PostGIS in staging/production environments. However, developer workstations and automated testing suites run without mandatory local PostgreSQL installations, benefiting from rapid, isolated in-memory testing.

### Problem
Directly coupling model definitions to `sqlalchemy.dialects.postgresql.UUID` and binding `create_async_engine(settings.DATABASE_URL)` at module load time prevented test suites from executing on machines lacking local PostgreSQL or `asyncpg` binaries.

### Alternatives
- **Option 1**: Force developers and CI to run a live PostgreSQL database for all test runs.
  - *Pros*: Tests only against target PostgreSQL.
  - *Cons*: High developer setup barrier, slower unit tests, fragile startup dependencies.
- **Option 2**: Use SQLAlchemy 2.0's native `sqlalchemy.Uuid(as_uuid=True)` and lazy engine initialization (`get_engine()`).
  - *Pros*: Compiles to native PostgreSQL `UUID` in production, seamlessly compiles to native/CHAR UUID in SQLite for instant test isolation, and avoids premature driver imports during imports.
  - *Cons*: Slight abstraction layer around engine access.

### Chosen Approach
Option 2: Use `sqlalchemy.Uuid(as_uuid=True)` across all models and initialize the database engine lazily on request in `app.core.database`.

### Reason
Enables zero-friction local testing and fast test suite execution (13 tests in ~1 second) while guaranteeing complete schema parity with PostgreSQL.

### Consequences
- **Positive**: All 12 tables and relationships can be verified in seconds without spinning up external containers.
- **Negative**: Dynamic engine creation requires calling `get_engine()` or using dependency injection.

### Related Implementation
- `backend/app/core/database.py`
- `backend/app/models/`
- `backend/tests/test_database.py`

### Related Commit
Pending database models commit.

---

## Decision: ADR-003 — Phone-First Authentication with Dual-Token JWT Lifecycles

- **Date**: 2026-09-11
- **Status**: Accepted

### Context
Rural micro-entrepreneurs across India primarily rely on mobile devices and frequently lack active email accounts. Traditional web email-verification flows create significant adoption friction. Furthermore, mobile internet connectivity in rural areas is intermittent, meaning frequent token expirations cause disruptive login prompts.

### Problem
How should ThinkForge design its authentication and session management architecture to maximize usability for rural users while maintaining robust security boundaries?

### Alternatives
- **Option 1**: Email-only registration with single-token JWT.
  - *Pros*: Standard web implementation pattern.
  - *Cons*: High friction for rural users who lack email addresses or rarely check them.
- **Option 2**: Phone-first authentication with dual-token JWT lifecycle (short-lived access token + long-lived refresh token).
  - *Pros*: Minimal user friction, aligns directly with rural demographic realities (E.164 phone identifier), enables smooth token refreshing (`POST /auth/refresh`) without frequent password prompts, and keeps access tokens short-lived (60 min) for security.
  - *Cons*: Requires managing refresh token verification and exchange logic.

### Chosen Approach
Option 2: Implement phone-first registration and login with bcrypt hashing and dual JWT tokens (60 min access, 7 days refresh).

### Reason
Directly satisfies the SIH26091 rural user requirements and the approved implementation plan.

### Consequences
- **Positive**: Seamless rural entrepreneur onboarding; frontend can silently refresh expired access tokens via `/api/v1/auth/refresh`.
- **Negative**: Client applications must securely store and handle two tokens.

### Related Implementation
- `backend/app/core/security.py`
- `backend/app/schemas/auth.py`
- `backend/app/api/v1/auth.py`
- `backend/tests/test_auth.py`

### Related Commit
Pending authentication module commit.

---

## Decision: ADR-004 — Geodesic Calculations, Bounding Box Pre-filtering, and Section 33 Privacy Fuzzing

- **Date**: 2026-09-11
- **Status**: Accepted

### Context
ThinkForge matches rural micro-entrepreneurs with local co-founders, machinery, raw material suppliers, and government hubs within a tight hyper-local radius (typically 15-50 km). Under Section 33 privacy and ethical AI mandates, exact domestic coordinates of home-based rural artisans must never be published openly to other users.

### Problem
How should spatial proximity matching and coordinate storage be designed to provide accurate radius querying while protecting private domestic locations?

### Alternatives
- **Option 1**: Rely purely on PostgreSQL PostGIS runtime functions (`ST_DWithin`, `ST_Distance`) and store/expose raw coordinates.
  - *Pros*: Leverages native spatial indices in PostgreSQL.
  - *Cons*: Cannot run fast in-memory SQLite unit tests without PostGIS binaries; fails Section 33 privacy mandates if raw coordinates are exposed to other users.
- **Option 2**: Hybrid approach:
  1. Pure Python Haversine geodesic calculation & bounding-box pre-filtering (`app/core/spatial.py`) for cross-dialect portability and unit testability.
  2. Bounding box coordinates generated in Python for database query optimization (`BETWEEN :min_lat AND :max_lat`).
  3. Deterministic coordinate fuzzing (`obfuscate_coordinates`) that perturbs exact GPS points within a safe 1-2 km radius before public display.

### Chosen Approach
Option 2: Hybrid geodesic calculations with bounding box pre-filtering and deterministic Section 33 coordinate fuzzing.

### Reason
Guarantees privacy for vulnerable rural micro-entrepreneurs while providing fast, reliable geospatial matching and 100% testable code without requiring an external GIS database engine during development.

### Consequences
- **Positive**: Privacy preserved; high testability; rapid distance calculations.
- **Negative**: Obfuscated public coordinates introduce up to 1-2 km of geographic fuzzing (intended by design).

### Related Implementation
- `backend/app/core/spatial.py`
- `backend/app/api/v1/profile.py`
- `backend/tests/test_spatial.py`

### Related Commit
Pending profile & spatial commit.

---

## Decision: ADR-005 — Teammate Contract Stubs & Decoupled Integration Architecture

- **Date**: 2026-09-11
- **Status**: Accepted

### Context
ThinkForge is developed by a multi-disciplinary 6-person team:
- Dhruv (Backend Core, DB, Auth)
- Aishwarya (AI Feasibility & Team Matching)
- Kesha (Financial Viability & Schemes)
- Smit (Ground Truth & Field Evidence)
- Madhav (Frontend Web Application)
- Harshanshu (Mobile Application)

Without clear, runnable API contracts, frontend/mobile developers cannot build interfaces, and domain developers cannot test their specialized algorithms in a unified environment.

### Problem
How should Dhruv expose backend endpoints for other team members without implementing their proprietary algorithms or blocking their future independent work?

### Alternatives
- **Option 1**: Wait for each teammate to complete their code before adding backend routers.
  - *Pros*: Avoids maintaining stubs.
  - *Cons*: Creates sequential team blockers; frontend and mobile teams cannot start UI integration; no common testing surface.
- **Option 2**: Create typed Pydantic contract schemas and lightweight baseline router stubs mounted directly under `/api/v1` (`businesses`, `partners`, `finance`, `evidence`).
  - *Pros*: Unblocks all 5 team members immediately; auto-generates comprehensive interactive Swagger OpenAPI specifications (`/docs`); provides a stable test suite ensuring contract stability; allows teammates to swap stubs for full implementations seamlessly.
  - *Cons*: Stubs must be replaced or enhanced as domain algorithms mature.

### Chosen Approach
Option 2: Create typed Pydantic contracts and lightweight baseline router stubs mounted into the primary FastAPI application router.

### Reason
Enables true parallel engineering across all 6 subteams with zero coordination friction.

### Consequences
- **Positive**: Complete OpenAPI schemas; 44 passing automated tests; frontend and mobile teams can develop immediately.
- **Negative**: Domain routers will be modified or extended by respective teammates in subsequent milestones.

### Related Implementation
- `backend/app/schemas/integration.py`
- `backend/app/api/v1/businesses.py`
- `backend/app/api/v1/partners.py`
- `backend/app/api/v1/finance.py`
- `backend/app/api/v1/evidence.py`
- `backend/tests/test_integration.py`

### Related Commit
Pending team integration commit.

---

## Decision: ADR-006 — Mobile OTP Authentication & In-Memory Rate Limiting

- **Date**: 2026-09-11
- **Status**: Accepted

### Context
Rural micro-entrepreneurs have high friction with alphanumeric passwords and password resets. Phone-based SMS OTP offers an intuitive, accessible authentication and registration journey. However, open SMS endpoints introduce vulnerabilities to SMS gateway abuse and brute-force credential stuffing without protective rate limiting.

### Problem
How can ThinkForge provide seamless mobile OTP authentication while defending against denial-of-wallet SMS flooding and brute-force attacks?

### Alternatives
- **Option 1**: External managed authentication provider (Firebase Auth / Auth0).
  - *Pros*: Offloads OTP infrastructure.
  - *Cons*: High vendor lock-in, recurring SMS costs, external cloud dependency, breaks self-contained local testing and offline compliance.
- **Option 2**: Native FastAPI OTP engine with in-memory TTL cache, cryptographic token generation (`secrets`), and sliding-window rate limiting dependency (`RateLimiter`).
  - *Pros*: Completely self-contained, zero external costs, 100% testable locally without SMS credits, protects against credential stuffing (10 req/min) and SMS flooding (5 req/min), seamless fallback for development (`999999`).
  - *Cons*: In multi-replica cloud environments, in-memory cache will need Redis backend substitution.

### Chosen Approach
Option 2: Native OTPManager with TTL and attempt quotas paired with FastAPI sliding-window rate limiter dependency.

### Reason
Maximizes rural user accessibility and security without creating costly external dependencies or blocking local CI/CD pipelines.

### Consequences
- **Positive**: Passwordless onboarding; instant phone verification; defense against brute-force attacks.
- **Negative**: For horizontal multi-instance scaling, Redis cache should be used.

### Related Implementation
- `backend/app/core/otp.py`
- `backend/app/core/rate_limiter.py`
- `backend/app/api/v1/auth.py`
- `backend/tests/test_otp.py`

### Related Commit
Pending containerization and OTP commit.






