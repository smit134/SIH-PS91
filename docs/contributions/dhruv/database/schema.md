# Database Schema Specification — ThinkForge

> **Current Status**: `Implemented`  
> *Note: All 12 core tables are defined in SQLAlchemy ORM models (`app/models/`), verified through 13 automated tests, and committed to Alembic revision `20260911_000000`.*

---

## 1. Schema Policy & Safety Rule

- **Source of Truth**: The database schema document strictly reflects tables that actually exist in code and migrations.
- Primary keys use cross-dialect `Uuid(as_uuid=True)` with automatic UUIDv4 generation.
- All timestamps (`created_at`, `updated_at`) store timezone-aware UTC datetimes.

---

## 2. Active Core Tables

### Table 1: `users`
- **Purpose**: Core user account entity storing phone identifier, password hash, and system role.
- **Primary Key**: `id` (UUID, default: `uuid.uuid4()`)
- **Columns**:
  | Column Name | Data Type | Nullable | Default | Constraints | Description |
  | :--- | :--- | :--- | :--- | :--- | :--- |
  | `id` | UUID | No | `uuid.uuid4()` | PRIMARY KEY | Unique identifier |
  | `phone` | String(20) | No | None | UNIQUE, INDEX | Primary contact identifier (E.164) |
  | `email` | String(255) | Yes | None | UNIQUE, INDEX | Optional email address |
  | `hashed_password` | String(255) | No | None | | Securely hashed password |
  | `role` | Enum(UserRole) | No | `ENTREPRENEUR` | | `ENTREPRENEUR`, `ADVISOR`, `ADMIN` |
  | `is_active` | Boolean | No | `True` | | Account active flag |
  | `is_verified` | Boolean | No | `False` | | Identity verification flag |
  | `created_at` | DateTime(tz) | No | `utcnow()` | | Account creation timestamp |
  | `updated_at` | DateTime(tz) | No | `utcnow()` | | Last update timestamp |
- **Relationships**:
  - `profile`: One-to-one with `Profile` (`cascade="all, delete-orphan"`)
  - `partner_profile`: One-to-one with `PartnerProfile` (`cascade="all, delete-orphan"`)
  - `audit_logs`: One-to-many with `AuditLog` (`cascade="all, delete-orphan"`)
- **Ownership / Privacy**: Passwords are never returned in schemas; phone numbers are masked in public views until mutual consent.

---

### Table 2: `profiles`
- **Purpose**: Entrepreneur capability profile capturing budget, geographic coordinates, language, and risk appetite.
- **Primary Key**: `id` (UUID)
- **Columns**:
  | Column Name | Data Type | Nullable | Default | Constraints | Description |
  | :--- | :--- | :--- | :--- | :--- | :--- |
  | `id` | UUID | No | `uuid.uuid4()` | PRIMARY KEY | Unique identifier |
  | `user_id` | UUID | No | None | UNIQUE, FK, INDEX | References `users.id` (ON DELETE CASCADE) |
  | `full_name` | String(100) | No | None | | Full name |
  | `language` | String(10) | No | `'hi'` | | Preferred language |
  | `latitude` | Float | Yes | None | | Latitude coordinate (WGS 84) |
  | `longitude` | Float | Yes | None | | Longitude coordinate (WGS 84) |
  | `approx_location_name`| String(255) | Yes | None | | Village / Taluka / District name |
  | `service_radius_km` | Integer | No | `10` | | Operating catchment radius (5-10 km) |
  | `available_capital` | BigInteger | No | `0` | | Available capital in INR |
  | `risk_tolerance` | Enum | No | `'MEDIUM'` | | `LOW`, `MEDIUM`, `HIGH` |
  | `experience_years` | Integer | No | `0` | | Commercial experience years |
  | `created_at` | DateTime(tz) | No | `utcnow()` | | Creation timestamp |
  | `updated_at` | DateTime(tz) | No | `utcnow()` | | Last update timestamp |
- **Relationships**:
  - `skills`: One-to-many with `UserSkill` (`cascade="all, delete-orphan"`)
  - `resources`: One-to-many with `UserResource` (`cascade="all, delete-orphan"`)

---

### Table 3: `skills`
- **Purpose**: Canonical taxonomy of production, marketing, craft, and business capabilities.
- **Primary Key**: `id` (UUID)
- **Columns**:
  | Column Name | Data Type | Nullable | Constraints | Description |
  | :--- | :--- | :--- | :--- | :--- |
  | `id` | UUID | No | PRIMARY KEY | Unique identifier |
  | `name` | String(100) | No | UNIQUE, INDEX | Skill title |
  | `category` | String(50) | No | INDEX | PRODUCTION, MARKETING, LOGISTICS, etc. |

---

### Table 4: `user_skills`
- **Purpose**: Mapping table linking entrepreneurs to skills with proficiency ratings.
- **Primary Key**: `id` (UUID)
- **Columns**:
  | Column Name | Data Type | Nullable | Constraints | Description |
  | :--- | :--- | :--- | :--- | :--- |
  | `id` | UUID | No | PRIMARY KEY | Unique identifier |
  | `profile_id` | UUID | No | FK, INDEX | References `profiles.id` (ON DELETE CASCADE) |
  | `skill_id` | UUID | No | FK, INDEX | References `skills.id` (ON DELETE CASCADE) |
  | `proficiency` | Enum | No | | `BEGINNER`, `INTERMEDIATE`, `EXPERT` |

---

### Table 5: `resources`
- **Purpose**: Taxonomy of physical assets (land, machinery, vehicles, shops).
- **Primary Key**: `id` (UUID)
- **Columns**:
  | Column Name | Data Type | Nullable | Constraints | Description |
  | :--- | :--- | :--- | :--- | :--- |
  | `id` | UUID | No | PRIMARY KEY | Unique identifier |
  | `name` | String(100) | No | UNIQUE, INDEX | Resource name |
  | `resource_type` | Enum | No | INDEX | `LAND`, `EQUIPMENT`, `VEHICLE`, `STORAGE`, `RAW_MATERIAL`, `SHOP` |

---

### Table 6: `user_resources`
- **Purpose**: Physical assets owned or accessible by an entrepreneur.
- **Primary Key**: `id` (UUID)
- **Columns**:
  | Column Name | Data Type | Nullable | Constraints | Description |
  | :--- | :--- | :--- | :--- | :--- |
  | `id` | UUID | No | PRIMARY KEY | Unique identifier |
  | `profile_id` | UUID | No | FK, INDEX | References `profiles.id` (ON DELETE CASCADE) |
  | `resource_id` | UUID | No | FK, INDEX | References `resources.id` (ON DELETE CASCADE) |
  | `details` | String(255) | Yes | | Capacity, model, or acreage specifications |

---

### Table 7: `business_categories`
- **Purpose**: Benchmarked business models with capital bounds, operating costs, and skill requirements.
- **Primary Key**: `id` (UUID)
- **Columns**:
  | Column Name | Data Type | Nullable | Constraints | Description |
  | :--- | :--- | :--- | :--- | :--- |
  | `id` | UUID | No | PRIMARY KEY | Unique identifier |
  | `name` | String(100) | No | UNIQUE | Business category name |
  | `code` | String(50) | No | UNIQUE, INDEX | Normalized code (e.g. HANDICRAFT, DAIRY) |
  | `description` | Text | No | | Detailed operational blueprint |
  | `min_capital` | BigInteger | No | | Minimum capital in INR |
  | `max_capital` | BigInteger | No | | Maximum capital in INR |
  | `typical_monthly_operating_cost` | BigInteger | No | | Estimated monthly OPEX in INR |
  | `typical_monthly_revenue` | BigInteger | No | | Estimated monthly revenue in INR |
  | `risk_level` | String(20) | No | | Inherent risk rating (LOW, MEDIUM, HIGH) |
  | `required_skills` | JSON | No | | Required skill codes list |
  | `required_resources`| JSON | No | | Required equipment/resource types list |
  | `break_even_months_est` | Integer | No | | Estimated break-even in months |
  | `is_active` | Boolean | No | | Active search availability |

---

### Table 8: `partner_profiles`
- **Purpose**: Partner seeker preferences and investment ranges.
- **Primary Key**: `id` (UUID)
- **Columns**:
  | Column Name | Data Type | Nullable | Constraints | Description |
  | :--- | :--- | :--- | :--- | :--- |
  | `id` | UUID | No | PRIMARY KEY | Unique identifier |
  | `user_id` | UUID | No | UNIQUE, FK, INDEX | References `users.id` (ON DELETE CASCADE) |
  | `investment_capacity_min` | BigInteger | No | | Min capital contribution in INR |
  | `investment_capacity_max` | BigInteger | No | | Max capital contribution in INR |
  | `verification_status` | Enum | No | | `BASIC`, `VERIFIED` |
  | `is_looking_for_partner`| Boolean | No | | Discovery visibility flag |

---

### Table 9: `partner_matches`
- **Purpose**: Calculated synergy matches and mutual-consent records.
- **Primary Key**: `id` (UUID)
- **Columns**:
  | Column Name | Data Type | Nullable | Constraints | Description |
  | :--- | :--- | :--- | :--- | :--- |
  | `id` | UUID | No | PRIMARY KEY | Unique identifier |
  | `user_id` | UUID | No | FK, INDEX | References `users.id` (ON DELETE CASCADE) |
  | `partner_user_id` | UUID | No | FK, INDEX | References `users.id` (ON DELETE CASCADE) |
  | `synergy_score` | Integer | No | | Synergy match score (0-100) |
  | `reasons` | JSON | No | | Complementary factor breakdown list |
  | `status` | Enum | No | | `PENDING`, `ACCEPTED`, `REJECTED` |
  | `initiated_by` | UUID | No | FK | User who triggered the request |

---

### Table 10: `schemes`
- **Purpose**: Government financing schemes (PMEGP, MUDRA, Stand-Up India, etc.).
- **Primary Key**: `id` (UUID)
- **Columns**:
  | Column Name | Data Type | Nullable | Constraints | Description |
  | :--- | :--- | :--- | :--- | :--- |
  | `id` | UUID | No | PRIMARY KEY | Unique identifier |
  | `scheme_name` | String(150) | No | UNIQUE | Full official title |
  | `short_code` | String(50) | No | UNIQUE, INDEX | Identifier code |
  | `description` | Text | No | | Objectives and benefits |
  | `eligibility_rules` | JSON | No | | Structured rule parameters |
  | `max_loan_amount` | BigInteger | No | | Maximum financing ceiling in INR |
  | `interest_rate_annual`| Float | No | | Base annual interest rate |
  | `subsidy_percentage`| Float | No | | Government subsidy proportion |
  | `tenure_months_max`| Integer | No | | Maximum loan tenure in months |
  | `required_documents`| JSON | No | | Mandatory application documents list |
  | `official_source_url`| String(255) | Yes | | Verification portal link |
  | `authority_name` | String(100) | No | | Issuing ministry / agency |
  | `is_active` | Boolean | No | | Active matching flag |

---

### Table 11: `evidence`
- **Purpose**: Hyper-local market, price, and competitor data tagged with reliability tiers.
- **Primary Key**: `id` (UUID)
- **Columns**:
  | Column Name | Data Type | Nullable | Constraints | Description |
  | :--- | :--- | :--- | :--- | :--- |
  | `id` | UUID | No | PRIMARY KEY | Unique identifier |
  | `source_name` | String(100) | No | INDEX | Udyam, e-NAM, Census, etc. |
  | `evidence_type` | Enum | No | INDEX | `PRICE`, `COMPETITOR`, `DEMAND`, `INFRASTRUCTURE`, `DEMOGRAPHIC` |
  | `reliability_class` | Enum | No | INDEX | `VERIFIED`, `DERIVED`, `ESTIMATED`, `UNKNOWN` |
  | `confidence_score` | Integer | No | | Reliability score (0-100) |
  | `latitude` | Float | Yes | | Anchor latitude |
  | `longitude` | Float | Yes | | Anchor longitude |
  | `radius_km` | Float | Yes | | Spatial scope in km |
  | `payload` | JSON | No | | Metric measurements and signal points |
  | `fetched_at` | DateTime(tz) | No | | Snapshot retrieval date |

---

### Table 12: `audit_logs`
- **Purpose**: Security audit trail tracking auth events, consent updates, and sensitive modifications.
- **Primary Key**: `id` (UUID)
- **Columns**:
  | Column Name | Data Type | Nullable | Constraints | Description |
  | :--- | :--- | :--- | :--- | :--- |
  | `id` | UUID | No | PRIMARY KEY | Unique identifier |
  | `user_id` | UUID | Yes | FK, INDEX | References `users.id` (ON DELETE SET NULL) |
  | `action` | String(100) | No | INDEX | Event type (e.g. AUTH_LOGIN, CONSENT_GRANTED) |
  | `resource_type` | String(50) | No | INDEX | Category (USER, PROFILE, PARTNER_MATCH) |
  | `resource_id` | String(100) | Yes | | Target entity ID |
  | `ip_address` | String(45) | Yes | | Client IP address |
  | `details` | JSON | No | | Metadata payload |
