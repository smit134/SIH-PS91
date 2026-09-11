# Authorization & Access Control — Dhruv's Contribution

> **Current Status**: `Implemented`  
> *Note: Role-based access control (`require_role`) and active account enforcement (`get_current_active_user`) implemented in `app/core/deps.py`.*

---

## 1. Roles & Permissions Hierarchy

ThinkForge defines three system roles:

| Role | Scope | Key Permissions |
| :--- | :--- | :--- |
| `ENTREPRENEUR` | Standard User | Manage own profile, view public business ideas, simulate finances, discover matched partners, request consent. |
| `ADVISOR` / `FACILITATOR` | Ecosystem Supporter | View consented entrepreneur profiles, review business blueprints, assist in scheme routing. |
| `ADMIN` | Platform Operator | Manage business category benchmarks, manage official scheme definitions, view system audit logs. |

---

## 2. User Ownership Principle

- **Strict Resource Ownership**: An entrepreneur can ONLY view, update, or delete their own data:
  - Profile metadata (`/api/v1/profile`)
  - Owned skills and assets (`/api/v1/profile/skills`, `/api/v1/profile/resources`)
  - Financial simulator parameters and projections
  - Personal business blueprint reports
- Accessing or modifying another user's private data results in `403 Forbidden`.

---

## 3. Protected Resources Matrix

| Resource | Accessible By | Restrictions / Privacy Boundary |
| :--- | :--- | :--- |
| `User Profile (Personal)` | Owner, Admin | Full details visible only to owner and admin. |
| `Partner Card (Public View)` | Authenticated Users | Obfuscated location (approximate village/district), masked contact information, no exact bank balances. |
| `Partner Contact Details` | Matched Partner | **MUTUAL CONSENT REQUIRED**: Phone/email released only after both parties explicitly confirm mutual interest. |
| `Business Categories` | All Authenticated | Publicly readable benchmark models. |
| `Financial Simulations` | Owner | Strictly private to the entrepreneur. |
| `Scheme Catalog` | All Authenticated | Publicly readable government scheme metadata. |
| `Audit Logs` | Admin Only | System security and audit trail. |

---

## 4. Access Check Implementation (`deps.py`)

Access checks are implemented as composable FastAPI dependencies:

```python
# Conceptual design for dependency guards:

def require_role(required_role: str):
    async def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role != required_role and current_user.role != "ADMIN":
            raise HTTPException(status_code=403, detail="Insufficient role permissions")
        return current_user
    return role_checker

async def verify_profile_owner(profile_id: UUID, current_user: User = Depends(get_current_user)):
    # Verifies that current_user is the owner of profile_id
    ...
```

---

## 5. Privacy Boundaries & Consent Workflow

Section 33 of `project.md` dictates strict privacy safeguards:

```text
[User A finds Partner B via Synergy Score]
             │
             ▼
[User A views masked Partner Card (Skills, Capital Range, Synergy Score, Approx Area)]
             │
             ▼
[User A requests contact sharing] ──► Status: PENDING_CONSENT
             │
             ▼
[Partner B reviews User A profile summary & accepts] ──► Status: MUTUAL_CONSENT_GRANTED
             │
             ▼
[Both users can now view contact information]
```

---

## 6. Verification & Implementation Notes
*(This document will be updated with concrete dependency definitions and security tests once implementation begins.)*
