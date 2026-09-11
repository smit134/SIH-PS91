# ThinkForge — SIH26091 Rural Business Advisory AI
## Backend Core, Database & Auth Logic (Dhruv's Scope)

### Executive Summary
ThinkForge is an AI-powered rural micro-entrepreneurship decision-support platform (SIH Problem Statement: SIH26091). 
**Dhruv** owns **Part 3: Backend — Core APIs, Database & Auth Logic (Strictly Backend)**.

Dhruv's responsibility is building the backend foundation:
- High-performance asynchronous FastAPI core backend.
- PostgreSQL 16 database with PostGIS for spatial radius/proximity operations and pgvector readiness for AI embeddings.
- Async SQLAlchemy 2.0 ORM models and Alembic database migration system.
- Secure Authentication & Session Management (Phone number + Password / OTP-ready, JWT Access & Refresh tokens).
- Role-based and ownership-based Authorization.
- Security and privacy safeguards (coordinate fuzzing, mutual-consent contact release, input sanitization).
- Base API contracts, OpenAPI specs, and domain routing interfaces for teammates:
  - **Madhav** (Frontend Auth & Dashboards)
  - **Harshanshu** (Frontend Visualizations & Maps)
  - **Aishwarya** (Opportunity & Partner Matching Engines)
  - **Kesha** (Financial Engine & Scheme Routing)
  - **Smit** (AI / RAG / Data Pipeline)

### Tech Stack
- **Language**: Python 3.13
- **Framework**: FastAPI (async ASGI) + Uvicorn
- **Database**: PostgreSQL 16 + PostGIS extension + pgvector
- **ORM**: SQLAlchemy 2.0 (asyncio with asyncpg)
- **Migrations**: Alembic
- **Validation**: Pydantic V2 / Pydantic Settings
- **Security**: PassLib (Argon2id/bcrypt), PyJWT / python-jose
- **Testing**: Pytest, pytest-asyncio, HTTPX

### Source Specifications
- [project.md](file:///c:/Users/Dhruv%20Valani/Desktop/SIH_project/SIH-91/project.md) (Sections 21.5, 21.6, 22, 31, 32, 33)
- [docs/contributions/dhruv/README.md](file:///c:/Users/Dhruv%20Valani/Desktop/SIH_project/SIH-91/docs/contributions/dhruv/README.md)
