# Database Migrations — Alembic Strategy & Workflow

> **Current Status**: `Implemented`  
> *Note: Alembic environment configured and baseline revision `20260911_000000` verified with `alembic heads`.*

---

## 1. Alembic Setup & Strategy

- **Tool**: Alembic (async configuration using `async_engine`).
- **Location**: `backend/alembic/`
- **Configuration**: `backend/alembic.ini` and `backend/alembic/env.py`.
- **Strategy**:
  - Single, linear revision tree (`head`). No divergent migration branches in version control.
  - Auto-generation of migration scripts via SQLAlchemy metadata comparison (`target_metadata = Base.metadata`).
  - Strict manual inspection of every auto-generated migration file prior to execution.
  - Geometry columns and PostGIS spatial extensions are explicitly handled in migration scripts.

---

## 2. Migration Naming Convention

Migration files follow a structured naming format:

```text
YYYYMMDD_HHMMSS_<descriptive_action>.py
```

---

## 3. Schema Change Workflow

Whenever a database schema change is needed:

1. **Modify ORM Models**: Update or add SQLAlchemy model classes under `backend/app/models/`.
2. **Generate Migration**:
   ```bash
   alembic revision --autogenerate -m "describe_change"
   ```
3. **Review Generated Code**:
   - Inspect the generated migration file under `alembic/versions/`.
   - Verify that `upgrade()` and `downgrade()` methods are complete, symmetric, and safe.
   - Verify index creation, constraint names, and data types.
4. **Apply Migration**:
   ```bash
   alembic upgrade head
   ```
5. **Verify Database State**:
   - Test queries against the updated database schema.
6. **Update Documentation**:
   - Update `docs/contributions/dhruv/database/schema.md` with new/modified tables.
   - Record the revision in `docs/contributions/dhruv/implementation-log.md`.

---

## 4. Upgrade & Downgrade Commands

### Applying Migrations (Upgrade)
- Apply all pending migrations to latest version:
  ```bash
  alembic upgrade head
  ```
- Upgrade by a single revision:
  ```bash
  alembic upgrade +1
  ```

### Reverting Migrations (Downgrade)
- Revert the most recent revision:
  ```bash
  alembic downgrade -1
  ```
- Revert to a specific revision ID:
  ```bash
  alembic downgrade <revision_id>
  ```

---

## 5. Migration Testing Procedure

Before committing any migration to version control, run the two-way migration test:

```text
Step 1: Apply migration       -> alembic upgrade head
Step 2: Roll back migration   -> alembic downgrade -1
Step 3: Re-apply migration    -> alembic upgrade head
```

---

## 6. Migration History

| Revision ID | Date | Description | Status |
| :--- | :--- | :--- | :---: |
| `20260911_000000` | 2026-09-11 | Initial core schema: 12 tables (`users`, `profiles`, `skills`, `user_skills`, `resources`, `user_resources`, `business_categories`, `partner_profiles`, `partner_matches`, `schemes`, `evidence`, `audit_logs`) | **Active (head)** |

