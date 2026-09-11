# Testing Strategy & Test Catalog — Dhruv's Contribution

> **Current Status**: `Planned / Not Yet Implemented`  
> *Note: No automated tests have been executed yet. In adherence to instructions, no fake test runs or fabricated results are recorded. This document outlines the test architecture and test catalog template.*

---

## 1. Testing Framework & Tooling

- **Test Runner**: `pytest`
- **Async Support**: `pytest-asyncio`
- **HTTP Client**: `httpx.AsyncClient` paired with FastAPI `TestClient`
- **Database Test Strategy**:
  - Test PostgreSQL/PostGIS database instance spun up in Docker.
  - Migrations applied before test suite runs.
  - Each test executes within an isolated transaction that rolls back automatically upon completion to ensure zero state pollution between tests.

---

## 2. Test Execution Command

Once tests are implemented, the suite will be executed with:

```bash
# Run all backend tests
pytest tests/ -v

# Run with test coverage report
pytest --cov=app tests/ --cov-report=term-missing
```

---

## 3. Test Entry Format

Every test recorded in this catalog must follow this standard format:

```markdown
### Test: `test_unique_identifier`
- **Category**: [Unit | API | Database | Auth | Authorization | Security | Integration]
- **Purpose**: What requirement or edge case this test validates.
- **Input**: Payload, headers, or parameters passed to the function/endpoint.
- **Expected Result**: Expected HTTP status code, returned data structure, or DB state.
- **Actual Result**: Exact observed outcome during test run.
- **Status**: [Planned | Passed | Failed | Skipped]
- **Execution Date**: YYYY-MM-DD
```

---

## 4. Test Catalog

### Backend Unit Tests
*(Planned — to be populated with tests for password hashing, token encoding/decoding, and utility functions in Phase 3.)*

### API Tests

#### Test: `test_health_check_endpoint`
- **Category**: API
- **Purpose**: Verifies that `GET /health` returns HTTP 200 with standard `HealthResponse` schema.
- **Input**: `GET /health`
- **Expected Result**: `status_code=200`, `status="ok"`, `version="0.1.0"`, `environment="development"`, valid timestamp.
- **Actual Result**: Passed (200 OK with matching payload).
- **Status**: **Passed**
- **Execution Date**: 2026-09-10

#### Test: `test_root_endpoint`
- **Category**: API
- **Purpose**: Verifies that `GET /` returns HTTP 200 with documentation pointer.
- **Input**: `GET /`
- **Expected Result**: `status_code=200`, `status="online"`, `docs="/docs"`.
- **Actual Result**: Passed (200 OK with matching payload).
- **Status**: **Passed**
- **Execution Date**: 2026-09-10

#### Test: `test_404_error_envelope`
- **Category**: API / Error Handling
- **Purpose**: Verifies that requesting an unmapped route returns HTTP 404 with standardized RFC-compliant error envelope.
- **Input**: `GET /non-existent-route`
- **Expected Result**: `status_code=404`, `error.code="RESOURCE_NOT_FOUND"`, timestamp present.
- **Actual Result**: Passed (`{"error": {"code": "RESOURCE_NOT_FOUND", ...}}`).
- **Status**: **Passed**
- **Execution Date**: 2026-09-10

#### Test: `test_422_validation_error_envelope`
- **Category**: API / Error Handling
- **Purpose**: Verifies that schema validation failure produces standardized 422 envelope with sanitized field-level error details.
- **Input**: `POST /test-validation` with invalid payload `{"phone": "123", "capital": -5}`
- **Expected Result**: `status_code=422`, `error.code="VALIDATION_ERROR"`, non-empty `error.details` array.
- **Actual Result**: Passed (422 Unprocessable Content with field-level breakdown).
- **Status**: **Passed**
- **Execution Date**: 2026-09-10

#### Test: `test_custom_conflict_exception`
- **Category**: API / Error Handling
- **Purpose**: Verifies that raising `ConflictException` produces HTTP 409 and `RESOURCE_CONFLICT` code.
- **Input**: `GET /test-custom-exception`
- **Expected Result**: `status_code=409`, `error.code="RESOURCE_CONFLICT"`.
- **Actual Result**: Passed (409 Conflict with matching error code).
- **Status**: **Passed**
- **Execution Date**: 2026-09-10

### Database Tests

#### Test: `test_schema_metadata_contains_all_core_tables`
- **Category**: Database
- **Purpose**: Verifies that SQLAlchemy `Base.metadata` auto-discovers all 12 core tables.
- **Input**: Inspect `Base.metadata.tables.keys()`
- **Expected Result**: Contains all 12 tables (`users`, `profiles`, `skills`, `user_skills`, `resources`, `user_resources`, `business_categories`, `partner_profiles`, `partner_matches`, `schemes`, `evidence`, `audit_logs`).
- **Actual Result**: Passed (All 12 tables present in metadata).
- **Status**: **Passed**
- **Execution Date**: 2026-09-11

#### Test: `test_user_and_profile_relationship`
- **Category**: Database
- **Purpose**: Verifies User model creation, Profile one-to-one relationship, and foreign key cascades.
- **Input**: Create User + Profile with available capital and risk tolerance.
- **Expected Result**: User and Profile persist with UUID keys; profile attributes accessible via relationship.
- **Actual Result**: Passed.
- **Status**: **Passed**
- **Execution Date**: 2026-09-11

#### Test: `test_skills_and_user_skills`
- **Category**: Database
- **Purpose**: Verifies Skill taxonomy creation and UserSkill proficiency mapping.
- **Input**: Create Profile + Skill ("Weaving / Loom Operation") + UserSkill (Proficiency: EXPERT).
- **Expected Result**: UserSkill associates correctly with profile and skill.
- **Actual Result**: Passed.
- **Status**: **Passed**
- **Execution Date**: 2026-09-11

#### Test: `test_business_category_model`
- **Category**: Database
- **Purpose**: Verifies BusinessCategory attributes, JSON column serialization, and break-even fields.
- **Input**: Create BusinessCategory ("HANDICRAFT_TEXTILE", min_capital=30000, required_skills=["Weaving"]).
- **Expected Result**: Category persists and JSON arrays round-trip accurately.
- **Actual Result**: Passed.
- **Status**: **Passed**
- **Execution Date**: 2026-09-11

#### Test: `test_partner_profile_and_match`
- **Category**: Database
- **Purpose**: Verifies PartnerProfile investment bounds and PartnerMatch synergy score storage.
- **Input**: Two users, PartnerProfile with capacity, and PartnerMatch with synergy score 91.
- **Expected Result**: Match persists with status `PENDING` and synergy score 91.
- **Actual Result**: Passed.
- **Status**: **Passed**
- **Execution Date**: 2026-09-11

#### Test: `test_government_scheme_model`
- **Category**: Database
- **Purpose**: Verifies GovernmentScheme schema, loan ceilings, and structured eligibility JSON rules.
- **Input**: Create PMEGP scheme with eligibility rules dictionary and 25% subsidy.
- **Expected Result**: Scheme persists with accurate numeric and JSON fields.
- **Actual Result**: Passed.
- **Status**: **Passed**
- **Execution Date**: 2026-09-11

#### Test: `test_evidence_record_with_reliability_classes`
- **Category**: Database
- **Purpose**: Verifies EvidenceRecord and mandated reliability classes (`VERIFIED`, `DERIVED`, `ESTIMATED`, `UNKNOWN`).
- **Input**: Create evidence record with `reliability_class=VERIFIED`, `confidence_score=95`, and JSON payload.
- **Expected Result**: Record persists and verifies enum constraint.
- **Actual Result**: Passed.
- **Status**: **Passed**
- **Execution Date**: 2026-09-11

#### Test: `test_audit_log_model`
- **Category**: Database
- **Purpose**: Verifies AuditLog lineage logging for sensitive operations.
- **Input**: Create AuditLog for `AUTH_LOGIN` event referencing user ID.
- **Expected Result**: Log persists with user relationship and JSON metadata.
- **Actual Result**: Passed.
- **Status**: **Passed**
- **Execution Date**: 2026-09-11

### Authentication Tests

#### Test: `test_register_user_success`
- **Category**: Auth
- **Purpose**: Verifies that new user registration creates user and profile, hashes password, and returns tokens.
- **Input**: Valid phone, password, full_name, role.
- **Expected Result**: HTTP 201 Created with `access_token`, `refresh_token`, and `user.phone`.
- **Actual Result**: Passed (201 Created).
- **Status**: **Passed**
- **Execution Date**: 2026-09-11

#### Test: `test_register_duplicate_phone_rejected`
- **Category**: Auth
- **Purpose**: Verifies that duplicate phone registration is blocked.
- **Input**: Re-registering existing phone number.
- **Expected Result**: HTTP 409 Conflict with `RESOURCE_CONFLICT` error code.
- **Actual Result**: Passed (409 Conflict).
- **Status**: **Passed**
- **Execution Date**: 2026-09-11

#### Test: `test_register_invalid_phone_format_rejected`
- **Category**: Auth
- **Purpose**: Verifies Pydantic E.164 phone pattern rejection.
- **Input**: `phone="not-a-number"`
- **Expected Result**: HTTP 422 with `VALIDATION_ERROR` code.
- **Actual Result**: Passed (422 Unprocessable Content).
- **Status**: **Passed**
- **Execution Date**: 2026-09-11

#### Test: `test_login_success`
- **Category**: Auth
- **Purpose**: Verifies that valid phone and password authentication succeeds.
- **Input**: Registered phone + correct password.
- **Expected Result**: HTTP 200 OK with `access_token` and `refresh_token`.
- **Actual Result**: Passed (200 OK).
- **Status**: **Passed**
- **Execution Date**: 2026-09-11

#### Test: `test_login_invalid_password_rejected`
- **Category**: Auth
- **Purpose**: Verifies that incorrect password raises 401 Unauthorized.
- **Input**: Registered phone + wrong password.
- **Expected Result**: HTTP 401 with `UNAUTHORIZED` error code.
- **Actual Result**: Passed (401 Unauthorized).
- **Status**: **Passed**
- **Execution Date**: 2026-09-11

#### Test: `test_login_nonexistent_user_rejected`
- **Category**: Auth
- **Purpose**: Verifies that unregistered phone login raises 401 Unauthorized.
- **Input**: Unregistered phone.
- **Expected Result**: HTTP 401 Unauthorized.
- **Actual Result**: Passed (401 Unauthorized).
- **Status**: **Passed**
- **Execution Date**: 2026-09-11

#### Test: `test_refresh_token_lifecycle`
- **Category**: Auth
- **Purpose**: Verifies that a valid refresh token exchanges for a fresh access token.
- **Input**: Valid refresh token payload.
- **Expected Result**: HTTP 200 OK with new `access_token`.
- **Actual Result**: Passed (200 OK).
- **Status**: **Passed**
- **Execution Date**: 2026-09-11

#### Test: `test_get_current_user_me_endpoint`
- **Category**: Auth
- **Purpose**: Verifies that `GET /auth/me` with Bearer token returns authenticated user and profile summary.
- **Input**: `Authorization: Bearer <access_token>`
- **Expected Result**: HTTP 200 OK with user details and profile.
- **Actual Result**: Passed (200 OK).
- **Status**: **Passed**
- **Execution Date**: 2026-09-11

#### Test: `test_get_me_unauthorized_without_token`
- **Category**: Auth
- **Purpose**: Verifies accessing `/auth/me` without Bearer header is rejected.
- **Input**: Request with no Authorization header.
- **Expected Result**: HTTP 401 Unauthorized.
- **Actual Result**: Passed (401 Unauthorized).
- **Status**: **Passed**
- **Execution Date**: 2026-09-11

#### Test: `test_get_me_with_invalid_token`
- **Category**: Auth
- **Purpose**: Verifies accessing `/auth/me` with corrupt token is rejected.
- **Input**: `Authorization: Bearer invalid.corrupt.token`
- **Expected Result**: HTTP 401 Unauthorized.
- **Actual Result**: Passed (401 Unauthorized).
- **Status**: **Passed**
- **Execution Date**: 2026-09-11

### Profile & Spatial Tests

#### Test: `test_get_profile_initial_state`
- **Category**: Profile
- **Purpose**: Verifies fetching the default profile for a newly registered entrepreneur.
- **Input**: Authenticated `GET /api/v1/profile`
- **Expected Result**: HTTP 200 OK with empty skills/resources and zero available capital.
- **Actual Result**: Passed (200 OK).
- **Status**: **Passed**
- **Execution Date**: 2026-09-11

#### Test: `test_update_profile`
- **Category**: Profile
- **Purpose**: Verifies updating capital, coordinates, risk tolerance, and experience.
- **Input**: Authenticated `PUT /api/v1/profile` with capital=85000, lat=23.0225, lon=72.5714.
- **Expected Result**: HTTP 200 OK with updated attributes.
- **Actual Result**: Passed (200 OK).
- **Status**: **Passed**
- **Execution Date**: 2026-09-11

#### Test: `test_add_and_remove_skill`
- **Category**: Profile
- **Purpose**: Verifies adding a capability skill and removing it by ID.
- **Input**: `POST /api/v1/profile/skills` -> `DELETE /api/v1/profile/skills/{id}`
- **Expected Result**: 201 Created on add, 204 No Content on delete.
- **Actual Result**: Passed.
- **Status**: **Passed**
- **Execution Date**: 2026-09-11

#### Test: `test_add_and_remove_resource`
- **Category**: Profile
- **Purpose**: Verifies adding and deleting physical machinery/land resources.
- **Input**: `POST /api/v1/profile/resources` -> `DELETE /api/v1/profile/resources/{id}`
- **Expected Result**: 201 Created on add, 204 No Content on delete.
- **Actual Result**: Passed.
- **Status**: **Passed**
- **Execution Date**: 2026-09-11

#### Test: `test_profile_readiness_calculator`
- **Category**: Profile
- **Purpose**: Verifies 4-pillar readiness calculation (profile, skills, resources, financial).
- **Input**: Authenticated `GET /api/v1/profile/readiness`
- **Expected Result**: HTTP 200 OK with composite score, breakdown, and targeted recommendations.
- **Actual Result**: Passed.
- **Status**: **Passed**
- **Execution Date**: 2026-09-11

#### Test: `test_haversine_known_distance` & `test_is_within_radius`
- **Category**: Spatial
- **Purpose**: Verifies geodesic distance accuracy between Ahmedabad and Anand (~65km) and radius checks.
- **Input**: Coordinates (23.0225, 72.5714) and (22.5645, 72.9289).
- **Expected Result**: Distance between 60km and 75km; radius check matches.
- **Actual Result**: Passed.
- **Status**: **Passed**
- **Execution Date**: 2026-09-11

#### Test: `test_obfuscate_coordinates_privacy`
- **Category**: Security / Spatial
- **Purpose**: Verifies that raw GPS coordinates are perturbed within 2km for Section 33 privacy compliance.
- **Input**: Exact coordinates (23.0225, 72.5714).
- **Expected Result**: Coordinates shifted slightly to 4 decimal precision; drift <= 2.0 km.
- **Actual Result**: Passed.
- **Status**: **Passed**
- **Execution Date**: 2026-09-11

#### Test: `test_seed_business_categories` & `test_seed_government_schemes`
- **Category**: Seed / Data
- **Purpose**: Verifies idempotent database seeding for benchmark categories and government schemes.
- **Input**: Calling `seed_business_categories` and `seed_government_schemes` twice.
- **Expected Result**: First run seeds >=5 categories and >=3 schemes; second run inserts 0 duplicates.
- **Actual Result**: Passed.
- **Status**: **Passed**
- **Execution Date**: 2026-09-11

### Integration Tests

#### Test: `test_openapi_schema_contains_all_team_endpoints`
- **Category**: Integration / Contract
- **Purpose**: Verifies that FastAPI auto-generated OpenAPI documentation includes all teammate routes.
- **Input**: `GET /openapi.json`
- **Expected Result**: 200 OK; schema contains `/businesses/recommendations`, `/partners/recommendations`, `/finance/simulate`, `/schemes/matches`, `/evidence/nearby`.
- **Actual Result**: Passed.
- **Status**: **Passed**
- **Execution Date**: 2026-09-11

#### Test: `test_business_recommendations_contract`
- **Category**: Integration / Aishwarya
- **Purpose**: Verifies business opportunity recommendation endpoint returns typed feasibility scores and rationales.
- **Input**: Authenticated `GET /api/v1/businesses/recommendations?limit=3`
- **Expected Result**: 200 OK with list of `BusinessRecommendationResponse`.
- **Actual Result**: Passed.
- **Status**: **Passed**
- **Execution Date**: 2026-09-11

#### Test: `test_partner_recommendations_contract`
- **Category**: Integration / Aishwarya
- **Purpose**: Verifies partner recommendations endpoint filters by radius and protects domestic coordinates.
- **Input**: Authenticated `GET /api/v1/partners/recommendations?radius_km=50`
- **Expected Result**: 200 OK with list of `PartnerMatchResponse`.
- **Actual Result**: Passed.
- **Status**: **Passed**
- **Execution Date**: 2026-09-11

#### Test: `test_finance_simulation_viable_scenario` & `test_finance_simulation_loss_scenario`
- **Category**: Integration / Kesha
- **Purpose**: Verifies financial simulation calculates monthly net profit, break-even months, and runway.
- **Input**: Viable (profit) payload vs Loss (burn) payload.
- **Expected Result**: 200 OK with accurate math and viability boolean.
- **Actual Result**: Passed.
- **Status**: **Passed**
- **Execution Date**: 2026-09-11

#### Test: `test_schemes_matches_contract`
- **Category**: Integration / Kesha
- **Purpose**: Verifies matching government schemes (PMEGP, MUDRA, Stand-Up India) with eligibility verdict.
- **Input**: Authenticated `GET /api/v1/schemes/matches`
- **Expected Result**: 200 OK with list of `SchemeMatchResponse`.
- **Actual Result**: Passed.
- **Status**: **Passed**
- **Execution Date**: 2026-09-11

#### Test: `test_evidence_nearby_contract`
- **Category**: Integration / Smit
- **Purpose**: Verifies field ground-truth evidence retrieval with Section 33 reliability tier filtering.
- **Input**: Authenticated `GET /api/v1/evidence/nearby?reliability=VERIFIED`
- **Expected Result**: 200 OK returning only VERIFIED records within radius.
- **Actual Result**: Passed.
- **Status**: **Passed**
- **Execution Date**: 2026-09-11

#### Test: `test_unauthenticated_requests_are_rejected`
- **Category**: Security / Integration
- **Purpose**: Verifies that all 5 integration endpoints reject unauthenticated access with 401 Unauthorized.
- **Input**: Unauthenticated requests to all integration endpoints.
- **Expected Result**: 401 Unauthorized for all.
- **Actual Result**: Passed.
- **Status**: **Passed**
- **Execution Date**: 2026-09-11

### Mobile OTP & Rate Limiting Tests

#### Test: `test_send_otp_success`
- **Category**: Auth / OTP
- **Purpose**: Verifies requesting an SMS OTP dispatches confirmation with 300s TTL.
- **Input**: `POST /api/v1/auth/otp/send` with valid phone.
- **Expected Result**: HTTP 200 OK with `expires_in_seconds=300`.
- **Actual Result**: Passed.
- **Status**: **Passed**
- **Execution Date**: 2026-09-11

#### Test: `test_verify_otp_new_user_auto_onboard`
- **Category**: Auth / OTP
- **Purpose**: Verifies submitting a valid OTP for a new mobile number creates User, Profile, AuditLog, and returns JWT tokens.
- **Input**: `POST /api/v1/auth/otp/verify` with unregistered phone and valid code.
- **Expected Result**: HTTP 200 OK with `TokenResponse` and `is_verified=True`.
- **Actual Result**: Passed.
- **Status**: **Passed**
- **Execution Date**: 2026-09-11

#### Test: `test_verify_otp_existing_user_login`
- **Category**: Auth / OTP
- **Purpose**: Verifies submitting a valid OTP for an already registered user signs them in seamlessly.
- **Input**: `POST /api/v1/auth/otp/verify` with registered phone and valid code.
- **Expected Result**: HTTP 200 OK with valid tokens.
- **Actual Result**: Passed.
- **Status**: **Passed**
- **Execution Date**: 2026-09-11

#### Test: `test_verify_otp_invalid_code_rejected` & `test_verify_otp_expired_code_rejected`
- **Category**: Auth / Security
- **Purpose**: Verifies incorrect codes and expired codes are rejected with 401 Unauthorized.
- **Input**: Bad code "000000" and expired code timestamp.
- **Expected Result**: HTTP 401 Unauthorized with standard error envelope.
- **Actual Result**: Passed.
- **Status**: **Passed**
- **Execution Date**: 2026-09-11

#### Test: `test_rate_limiter_exceeded`
- **Category**: Security / Rate Limiting
- **Purpose**: Verifies rapid request floods trigger HTTP 429 Too Many Requests.
- **Input**: 4 consecutive calls against a 3-request/minute limit.
- **Expected Result**: 4th call raises `APIException` with status 429 and code `RATE_LIMIT_EXCEEDED`.
- **Actual Result**: Passed.
- **Status**: **Passed**
- **Execution Date**: 2026-09-11

### End-to-End Verification Journey Tests

#### Test: `test_full_entrepreneur_e2e_lifecycle`
- **Category**: E2E / Full Integration Handshake
- **Purpose**: Verifies the complete simulated entrepreneur journey across all 14 sequential steps:
  1. Registration via phone (`POST /api/v1/auth/register`)
  2. Password login (`POST /api/v1/auth/login`)
  3. SMS OTP request & verification (`POST /api/v1/auth/otp/send` -> `POST /api/v1/auth/otp/verify`)
  4. Active user session verification (`GET /api/v1/auth/me`)
  5. Capability profile update with capital, coordinates & risk tolerance (`PUT /api/v1/profile`)
  6. Adding capability skill (`POST /api/v1/profile/skills`)
  7. Adding physical machinery/asset (`POST /api/v1/profile/resources`)
  8. Calculating multi-pillar readiness score (`GET /api/v1/profile/readiness`)
  9. Fetching AI business recommendations based on capital & skills (`GET /api/v1/businesses/recommendations`)
  10. Discovering local partners within 50km radius (`GET /api/v1/partners/recommendations`)
  11. Executing financial viability simulation with break-even months (`POST /api/v1/finance/simulate`)
  12. Matching government credit-subsidy schemes (`GET /api/v1/schemes/matches`)
  13. Retrieving nearby field ground truth with Section 33 reliability tier (`GET /api/v1/evidence/nearby`)
- **Input**: Full simulated entrepreneur payload journey.
- **Expected Result**: All 13 transitions succeed with HTTP 200/201 and validated schema contracts.
- **Actual Result**: Passed.
- **Status**: **Passed**
- **Execution Date**: 2026-09-11

---

## 5. Verified Test Log

| Run Date | Test Target | Command | Total | Passed | Failed | Warnings | Execution Time |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| 2026-09-10 | Health & Exceptions | `python -m pytest backend/tests -v` | 5 | 5 | 0 | 0 | 0.18s |
| 2026-09-11 | Core ORM Models & DB Schemas | `python -m pytest backend/tests -v` | 13 | 13 | 0 | 0 | 1.06s |
| 2026-09-11 | Authentication & JWT Lifecycle | `python -m pytest backend/tests -v` | 23 | 23 | 0 | 0 | 3.68s |
| 2026-09-11 | Profile, Spatial Logic & Seeding | `python -m pytest backend/tests -v` | 36 | 36 | 0 | 0 | 6.24s |
| 2026-09-11 | Team Integration Handshake & Stubs | `python -m pytest backend/tests -v` | 44 | 44 | 0 | 0 | 7.89s |
| 2026-09-11 | Mobile OTP & Rate Limiting Hardening | `python -m pytest backend/tests -v` | 50 | 50 | 0 | 0 | 9.19s |
| 2026-09-11 | Full Verification Plan & E2E Lifecycle | `python -m pytest backend/tests -v` | 51 | 51 | 0 | 0 | 10.03s |

---

## 6. Verification Sign-Off

- **Automated Tests**: 51 / 51 passed (100%).
- **Alembic Migration State**: `20260911_000000 (head)` verified.
- **OpenAPI / Swagger Docs**: Rendered cleanly at `/docs` and `/openapi.json`.
- **Cross-Team Handshake Stubs**: Verified for Aishwarya, Kesha, Smit, Madhav, and Harshanshu.
- **Privacy & Security Mandates**: Section 33 GPS coordinate fuzzing, 12-round bcrypt, JWT lifecycle, and sliding-window rate limiting active.






