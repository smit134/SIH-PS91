---
name: project-documentation
description: "Maintain live, verified engineering documentation for Dhruv's scope (Backend Core, Database & Auth Logic) in ThinkForge"
---

# Project Documentation Skill — Dhruv's Contribution

## Objective
Enforce the **Live Documentation Rule** for all engineering tasks in Dhruv's scope:
```text
PLAN → IMPLEMENT → TEST → DOCUMENT → VERIFY → COMMIT
```
Whenever a task in Dhruv's domain (FastAPI, PostgreSQL/PostGIS, Alembic, Auth, Security, API conventions) is executed, this skill ensures that documentation under `docs/contributions/dhruv/` is systematically kept up-to-date with reality.

---

## Documentation Mapping Rules

When modifying or implementing code, update only the relevant documentation files:

| Implementation Action | Required Documentation Updates |
| :--- | :--- |
| **Any completed task or milestone** | `docs/contributions/dhruv/implementation-log.md` (append new entry following the template) |
| **FastAPI router, service, middleware, dependency** | `docs/contributions/dhruv/backend/fastapi.md`<br>`docs/contributions/dhruv/backend/api-conventions.md`<br>`docs/contributions/dhruv/backend/error-handling.md` |
| **SQLAlchemy model, database table, or index** | `docs/contributions/dhruv/database/schema.md`<br>`docs/contributions/dhruv/database/architecture.md` (if architecture altered) |
| **Alembic migration revision created or applied** | `docs/contributions/dhruv/database/migrations.md`<br>`docs/contributions/dhruv/database/schema.md` |
| **Authentication, JWT, password hashing, login logic** | `docs/contributions/dhruv/authentication/authentication.md`<br>`docs/contributions/dhruv/security/security.md` |
| **Authorization, ownership check, role guard, privacy rule** | `docs/contributions/dhruv/authentication/authorization.md`<br>`docs/contributions/dhruv/security/security.md` |
| **Security control or privacy boundary implemented** | `docs/contributions/dhruv/security/security.md` (move from Planned to Implemented) |
| **Automated unit, API, database, or security test run** | `docs/contributions/dhruv/testing/testing.md` (record input, expected, actual, and status) |
| **Architectural or engineering decision made** | `docs/contributions/dhruv/decisions/decisions.md` (record ADR with context and trade-offs) |

---

## Strict Behavioral Constraints

1. **Repository is the Source of Truth**:
   - Never document a feature as "Implemented" unless the code exists in the repository and has been verified.
   - Do not generate fictional test results, fake endpoints, or unapplied database tables.
2. **Strict Scope Isolation**:
   - Only modify documentation inside `docs/contributions/dhruv/`.
   - Do NOT modify `project.md`.
   - Do NOT create or modify documentation for other team members (Madhav, Harshanshu, Aishwarya, Kesha, Smit).
3. **Atomic Documentation**:
   - Documentation updates are considered a mandatory part of task completion before committing.
