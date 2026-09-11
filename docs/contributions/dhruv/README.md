# Dhruv — Backend Core, Database & Auth Logic

## Role
Backend backbone for the ThinkForge platform.

## Responsibility
As defined in Section 31 of [project.md](../../../project.md) (Part 3: Backend — Core APIs, Database & Auth Logic), Dhruv is strictly responsible for:
- FastAPI backend application architecture, configuration, and middleware.
- PostgreSQL and PostGIS spatial database design, setup, and relational models.
- Async SQLAlchemy database access layer and connection pooling.
- Alembic database migration management.
- Authentication API, credential security, and session/JWT management.
- Authorization, resource-level ownership, and role-based access control.
- Security and privacy controls (input validation, location fuzzing, mutual-consent privacy, audit logging).
- Base API contracts, conventions, and error handling standards.
- Backend infrastructure, spatial queries, and model interfaces required by teammates (Aishwarya, Kesha, Smit, Madhav, Harshanshu).

## Modules Owned
- **FastAPI backend foundation**: Core app, routing, dependency injection, middleware, error handlers.
- **Database**: PostgreSQL 16 + PostGIS spatial layer + pgvector compatibility.
- **Migrations**: Alembic environment, linear revision tracking, upgrade/downgrade workflows.
- **Authentication**: Registration, login, token lifecycle (JWT access/refresh), session management.
- **Authorization**: User ownership checks, role permissions, privacy boundaries.
- **Security**: Password hashing, secret management, CORS, rate-limiting, audit logs, privacy controls.
- **Base API contracts**: Standardized request/response structures, error formats, pagination, OpenAPI docs.

## Documentation Map
All documentation for Dhruv's assigned scope is maintained under this isolated contribution tree:

- **Overview & Engineering Log**:
  - [README.md](file:///c:/Users/Dhruv%20Valani/Desktop/SIH_project/SIH-91/docs/contributions/dhruv/README.md) — Scope, ownership, and current status.
  - [implementation-log.md](file:///c:/Users/Dhruv%20Valani/Desktop/SIH_project/SIH-91/docs/contributions/dhruv/implementation-log.md) — Chronological engineering log of tasks, changes, and commits.
- **Backend Architecture & Conventions**:
  - [backend/fastapi.md](file:///c:/Users/Dhruv%20Valani/Desktop/SIH_project/SIH-91/docs/contributions/dhruv/backend/fastapi.md) — Application structure, lifecycle, configuration, and services.
  - [backend/api-conventions.md](file:///c:/Users/Dhruv%20Valani/Desktop/SIH_project/SIH-91/docs/contributions/dhruv/backend/api-conventions.md) — URL standards, HTTP methods, pagination, schemas, and naming conventions.
  - [backend/error-handling.md](file:///c:/Users/Dhruv%20Valani/Desktop/SIH_project/SIH-91/docs/contributions/dhruv/backend/error-handling.md) — Error classifications, response envelope, status codes, and logging.
- **Database Layer**:
  - [database/architecture.md](file:///c:/Users/Dhruv%20Valani/Desktop/SIH_project/SIH-91/docs/contributions/dhruv/database/architecture.md) — PostgreSQL, PostGIS, SQLAlchemy 2.0 async, pooling, transactions.
  - [database/schema.md](file:///c:/Users/Dhruv%20Valani/Desktop/SIH_project/SIH-91/docs/contributions/dhruv/database/schema.md) — Table definitions, columns, constraints, foreign keys, and indexes.
  - [database/migrations.md](file:///c:/Users/Dhruv%20Valani/Desktop/SIH_project/SIH-91/docs/contributions/dhruv/database/migrations.md) — Alembic configuration, revision tracking, and migration workflows.
- **Authentication & Authorization**:
  - [authentication/authentication.md](file:///c:/Users/Dhruv%20Valani/Desktop/SIH_project/SIH-91/docs/contributions/dhruv/authentication/authentication.md) — Registration, credentials validation, JWT issuance, token lifecycle.
  - [authentication/authorization.md](file:///c:/Users/Dhruv%20Valani/Desktop/SIH_project/SIH-91/docs/contributions/dhruv/authentication/authorization.md) — Resource ownership, role-based gates, and privacy boundaries.
- **Security & Privacy**:
  - [security/security.md](file:///c:/Users/Dhruv%20Valani/Desktop/SIH_project/SIH-91/docs/contributions/dhruv/security/security.md) — Security controls, input validation, hashing, CORS, and privacy rules.
- **Testing**:
  - [testing/testing.md](file:///c:/Users/Dhruv%20Valani/Desktop/SIH_project/SIH-91/docs/contributions/dhruv/testing/testing.md) — Unit, integration, database, auth, and security test catalog.
- **Architecture Decisions**:
  - [decisions/decisions.md](file:///c:/Users/Dhruv%20Valani/Desktop/SIH_project/SIH-91/docs/contributions/dhruv/decisions/decisions.md) — Architectural Decision Records (ADRs).

## Current Status

| Module / Area | Status | Notes |
| :--- | :--- | :--- |
| Documentation Infrastructure | **Implemented** | Complete documentation directory structure, logs, and ADRs established. |
| FastAPI Backend Foundation | **Implemented** | Application factory, Pydantic BaseSettings, CORS, error envelope, `/health`, `/` implemented and tested. |
| PostgreSQL / PostGIS Database | **Implemented** | 12 core ORM models, async engine, session dependency, and cross-dialect portability implemented and tested. |
| Alembic Migrations | **Implemented** | Migration environment and initial baseline revision `20260911_000000 (head)` established. |
| Authentication & Session/JWT | **Implemented** | Phone-first register, login, refresh, `/auth/me`, bcrypt hashing, dual JWT lifecycle implemented and tested. |
| Containerization & Orchestration | **Implemented** | Multi-stage Dockerfile and docker-compose.yml for PostGIS 16 + FastAPI service. |
| Mobile OTP Authentication | **Implemented** | Passwordless SMS OTP generation, 5-min TTL, attempt limiting, and auto-onboarding (`/auth/otp/send`, `/auth/otp/verify`). |
| Request Rate Limiting | **Implemented** | Sliding-window in-memory rate limiting defending against credential stuffing and SMS flooding. |
| Automated Test Suite | **Implemented** | 50 comprehensive tests passing across 7 test modules (100% pass rate in 9.19s). |


