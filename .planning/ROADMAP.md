# Roadmap — Dhruv's Backend Delivery

## Overview
This roadmap organizes Dhruv's backend scope into 5 progressive, independently verifiable phases.

---

### Phase 1: Backend Foundation & Configuration
- **Goal**: Setup FastAPI core application architecture, configuration management, exception hierarchy, error envelopes, and automated test foundation.
- **Deliverables**:
  - `backend/app/config.py` (Pydantic BaseSettings)
  - `backend/app/core/exceptions.py` (Standard exception classes and global handlers)
  - `backend/app/schemas/common.py` (Standard response envelope)
  - `backend/app/main.py` (FastAPI app factory, CORS, health endpoint)
  - `backend/tests/` (Pytest setup and health check tests)
- **Status**: Planned

---

### Phase 2: Database Layer & PostGIS Models
- **Goal**: Establish async SQLAlchemy 2.0 database engine, PostGIS spatial models, Alembic migration environment, and initial baseline schema.
- **Deliverables**:
  - `backend/app/core/database.py` (Async engine, session factory, `get_db`)
  - `backend/app/models/` (User, Profile, Skill, Resource, BusinessCategory, Partner, Match, Evidence, AuditLog)
  - `backend/alembic/` (Alembic async configuration, initial migration revision)
  - Database schema documentation update in `docs/contributions/dhruv/database/schema.md`
- **Status**: Planned

---

### Phase 3: Authentication, Session & Security Controls
- **Goal**: Implement password hashing, JWT access/refresh token generation, authentication endpoints, and role/ownership security guards.
- **Deliverables**:
  - `backend/app/core/security.py` (Password hashing, JWT utilities)
  - `backend/app/core/deps.py` (`get_current_user`, `require_role`, ownership verification)
  - `backend/app/schemas/auth.py` (Pydantic auth DTOs)
  - `backend/app/api/v1/auth.py` (`/auth/register`, `/auth/login`, `/auth/me`, `/auth/refresh`)
  - Privacy controls (location obfuscation, mutual-consent contact release logic)
  - Automated auth tests (`tests/test_auth.py`)
- **Status**: Planned

---

### Phase 4: Profile Management, Spatial Logic & Seeding
- **Goal**: Implement complete Entrepreneur Capability Profile CRUD, PostGIS spatial query utilities, and pre-populated seed data for MVP business categories.
- **Deliverables**:
  - `backend/app/schemas/profile.py` (Profile, Skill, Resource DTOs)
  - `backend/app/api/v1/profile.py` (Profile CRUD, skills/resources management, readiness calculator)
  - Spatial helpers for radius queries (`ST_DWithin`)
  - `backend/app/seed/` (Seed dataset with 5 benchmark rural business categories)
  - Automated profile and spatial tests (`tests/test_profile.py`)
- **Status**: Planned

---

### Phase 5: Team Integration Contracts & Verification
- **Goal**: Provide clean router mounts, Pydantic DTO contracts, and OpenAPI documentation for Aishwarya, Kesha, Smit, Madhav, and Harshanshu.
- **Deliverables**:
  - `backend/app/api/v1/businesses.py` (Opportunity engine contract)
  - `backend/app/api/v1/partners.py` (Partner engine contract)
  - `backend/app/api/v1/finance.py` (Financial simulator contract)
  - `backend/app/api/v1/schemes.py` (Scheme matching contract)
  - `backend/app/api/v1/evidence.py` (Evidence retrieval contract)
  - Full end-to-end integration test suite
  - Final documentation and walkthrough synchronization
- **Status**: Planned
