# Database Architecture — Dhruv's Contribution

> **Current Status**: `Implemented`  
> *Note: PostgreSQL 16 + PostGIS compatible ORM architecture, lazy engine initialization, async session dependency, and cross-dialect models implemented and verified.*

---

## 1. Database Technology Stack

- **Engine**: PostgreSQL 16.
- **Extensions**:
  - `postgis`: Enables geospatial data types (`GEOMETRY`, `GEOGRAPHY`), spatial indexing (`GIST`), and distance/containment calculations (`ST_DWithin`, `ST_Distance`).
  - `vector` (pgvector): Enables dense vector embeddings storage and similarity search (prepared for Smit's RAG module).
- **ORM / Driver**:
  - `SQLAlchemy 2.0` in strict asynchronous mode (`asyncio`).
  - `asyncpg`: High-performance asynchronous PostgreSQL database driver for Python.

---

## 2. PostGIS Spatial Layer

ThinkForge requires hyper-local geospatial intelligence (evaluating business feasibility and partner matching within a 5–10 km radius):

- **Data Types**: Coordinates stored as `Geography(Point, 4326)` (WGS 84 coordinate system using latitude/longitude).
- **Spatial Indexing**: `GIST` (Generalized Search Tree) indexes applied to all spatial columns (`location_geom`).
- **Spatial Queries**:
  - Proximity matching: `ST_DWithin(a.location_geom, b.location_geom, radius_in_meters)` allows index-accelerated range queries.
  - GeoJSON generation: `ST_AsGeoJSON(location_geom)` allows direct conversion to GeoJSON for Harshanshu's frontend MapLibre maps.

---

## 3. Database Access Layer

- **Session Management**:
  - `async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)` creates thread-safe request-scoped sessions.
  - Injected into FastAPI routes via the `get_db()` dependency.
- **Base Model**:
  - `DeclarativeBase` subclass providing common columns (`id` as UUID primary key, `created_at`, `updated_at`).

---

## 4. Entity Relationships & Constraints

- **Foreign Key Integrity**:
  - Enforced at the database level with strict `ON DELETE` rules (e.g., `CASCADE` for user profile children, `RESTRICT` for audit logs).
- **Integrity Constraints**:
  - `UNIQUE` constraints on user phone number and email.
  - `CHECK` constraints on financial inputs (e.g., non-negative costs and revenues) and scores (e.g., `0 <= score <= 100`).

---

## 5. Indexes Strategy

- **Primary Keys**: B-tree index on all UUID primary keys.
- **Foreign Keys**: B-tree index on all foreign key columns to eliminate query bottlenecks during joins.
- **Spatial Data**: GIST indexes on all geography/geometry columns.
- **Categorical & Search Columns**: Composite or partial indexes on frequently filtered fields (e.g., `status`, `role`).

---

## 6. Transactions & Connection Management

- **Transaction Scope**: 
  - Each HTTP request executes within an isolated transaction.
  - FastAPI dependency yields session, commits upon successful response generation, and executes `session.rollback()` if an exception occurs.
- **Connection Pool Configuration**:
  - `pool_size`: 10 (base active connections).
  - `max_overflow`: 20 (surge connections).
  - `pool_timeout`: 30 seconds.
  - `pool_recycle`: 1800 seconds (prevents stale TCP connections).
  - `pool_pre_ping`: True (verifies connection health before dispensing).

---

## 7. Verification & Updates
*This architecture will be updated with actual connection metrics and verified benchmarks once the database environment is deployed.*
