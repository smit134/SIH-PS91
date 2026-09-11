# API Conventions & Standards — ThinkForge Backend

> **Current Status**: `Planned / Proposed Standards (Not Yet Implemented)`  
> *Note: These conventions define the integration contract for all ThinkForge API endpoints developed by Dhruv and teammates.*

---

## 1. URL Structure & Versioning

- Base URL: `/api/v1`
- Plural nouns for resource collections:
  - `/api/v1/users`
  - `/api/v1/businesses`
  - `/api/v1/partners`
  - `/api/v1/schemes`
  - `/api/v1/evidence`
- Actions that do not map to pure CRUD use descriptive verbs:
  - `/api/v1/auth/login`
  - `/api/v1/auth/register`
  - `/api/v1/finance/simulate`
  - `/api/v1/partners/recommendations`
- Kebab-case for multi-word path segments: `/api/v1/partner-matches`

---

## 2. HTTP Methods

| Method | Idempotent | Safe | Typical Purpose | Expected Success Code |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | Yes | Yes | Retrieve a resource or list of resources | `200 OK` |
| `POST` | No | No | Create a new resource or run an operation (simulation/login) | `201 Created` or `200 OK` |
| `PUT` | Yes | No | Replace/update an entire resource | `200 OK` |
| `PATCH` | No | No | Partial update of a resource | `200 OK` |
| `DELETE` | Yes | No | Delete a resource | `200 OK` or `204 No Content` |

---

## 3. Request Validation

- All request bodies are strictly validated via Pydantic schemas.
- Invalid data types, missing required fields, or constraint failures automatically produce an HTTP `422 Unprocessable Entity`.
- JSON payloads must be encoded with `Content-Type: application/json`.

---

## 4. Response Format

### Standard Success Response (Resource / Object)
Direct serialization of the requested resource or a standard envelope:
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "phone": "+919876543210",
  "role": "ENTREPRENEUR",
  "created_at": "2026-09-10T12:00:00Z"
}
```

### Paginated List Response
For collection endpoints returning lists:
```json
{
  "items": [ ... ],
  "total": 45,
  "page": 1,
  "page_size": 10,
  "total_pages": 5
}
```

---

## 5. Error Format

All error responses strictly adhere to a consistent error schema across all endpoints:

```json
{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "The requested business category does not exist.",
    "details": null,
    "timestamp": "2026-09-10T12:00:00Z"
  }
}
```

### Validation Error Format (422)
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request parameters.",
    "details": [
      {
        "loc": ["body", "phone"],
        "msg": "Invalid phone number format",
        "type": "value_error"
      }
    ],
    "timestamp": "2026-09-10T12:00:00Z"
  }
}
```

---

## 6. HTTP Status Codes

- `200 OK`: Successful retrieval or synchronous operation.
- `201 Created`: Resource successfully created.
- `204 No Content`: Successful deletion or operation with empty response.
- `400 Bad Request`: Client error (malformed request, business logic violation).
- `401 Unauthorized`: Missing or invalid authentication token.
- `403 Forbidden`: Authenticated user lacks permission to access the resource.
- `404 Not Found`: Target resource does not exist.
- `409 Conflict`: Resource collision (e.g., duplicate phone number).
- `422 Unprocessable Entity`: Request body or parameter validation error.
- `500 Internal Server Error`: Unhandled server-side error.

---

## 7. Pagination

- Default pagination parameters for list endpoints:
  - `page` (integer, default: `1`, min: `1`)
  - `page_size` (integer, default: `20`, max: `100`)
- Alternatively, cursor-based pagination for large data feeds:
  - `cursor` (string)
  - `limit` (integer)

---

## 8. Authentication & Authorization Requirements

- Protected endpoints require an HTTP header:
  `Authorization: Bearer <JWT_ACCESS_TOKEN>`
- Missing or malformed header returns `401 Unauthorized`.
- Endpoints enforcing role checks or ownership verify that the authenticated user owns the accessed resource or has `ADMIN` privileges; otherwise, `403 Forbidden` is returned.

---

## 9. Naming Conventions

- **JSON field names**: `snake_case` (e.g., `user_id`, `created_at`, `risk_tolerance`).
- **URL path segments**: `kebab-case` (e.g., `partner-matches`).
- **Query parameters**: `snake_case` (e.g., `?page_size=10&risk_tolerance=low`).
- **HTTP Headers**: `Kebab-Case` (e.g., `Authorization`, `X-Request-ID`).
