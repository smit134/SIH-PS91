# ThinkForge — Intelligence Layer (Part 4: Aishwarya)

## 📌 Overview

This repository subfolder implements the complete **Intelligence, Opportunity & Partner Engines** assigned to **Aishwarya (Part 4)** in [project.md](../project.md).

It provides deterministic, inspectable scoring algorithms, geospatial proximity queries, capability gap logic, and reverse business search services for the **ThinkForge AI Rural Advisory Platform (SIH26091)**.

---

## 🚀 Key Modules & Features Implemented

### 1. Opportunity Scoring & Explainability Engine (`app/engines/opportunity_engine.py`)
- **7-Factor Weighted Opportunity Fit Formula** (Section 24):
  $$\text{Fit Score} = 0.20 \times \text{CapitalFit} + 0.20 \times \text{SkillFit} + 0.15 \times \text{ResourceFit} + 0.20 \times \text{LocalOpportunity} + 0.10 \times \text{MarketAccess} + 0.10 \times \text{MarginPotential} + 0.05 \times \text{RiskSuitability}$$
- **Explainability Generation**:
  - `why_recommended`: Direct matching strengths
  - `why_not_perfect`: Missing skills / distribution gaps
  - `why_not_this_business`: Explicit rejection rationale for unviable categories (e.g. Budget < Min Capital requirement)
  - `confidence_limitations`: Evidence boundaries and proxy warnings
- **USP #2: Reverse Business Search ("Resource → Business Engine")**:
  - Automatically identifies all viable businesses from available assets and skills.
- **Side-by-Side Business Comparison Matrix** (Section 13).

### 2. Capability Dashboard & Gap Analysis (`app/engines/capability_gap_engine.py`)
- Evaluates 6 Core Capability Pillars:
  1. `Production`
  2. `Capital`
  3. `Marketing`
  4. `Distribution`
  5. `Technology`
  6. `Management`
- Identifies **Biggest Capability Gaps** (e.g., Marketing, Working Capital) to feed the Partner Engine.

### 3. Complementary Partner Matching & Synergy Scoring (`app/engines/partner_engine.py`)
- **USP #1: AI Business Partner Finder** (Section 6 & 25):
  - Matches **One user's missing capability with another candidate's strength**.
  - **6-Factor Synergy Scoring**:
    $$\text{Synergy} = 0.30 \times \text{SkillComplementarity} + 0.20 \times \text{CapitalCompatibility} + 0.15 \times \text{ResourceComplementarity} + 0.15 \times \text{SharedInterest} + 0.10 \times \text{LocationProximity} + 0.10 \times \text{ExperienceCompatibility}$$
- **Privacy-Preserving Presentation** (Section 6, 15, 33):
  - Masks phone numbers and exact coordinates; displays approximate area and verification status (`BASIC` / `VERIFIED`).
  - Implements **Mutual-Interest Consent Flow** (`POST /api/intelligence/partner/request-contact`).

### 4. Geospatial Proximity & Hyper-Local Evidence Layer (`app/engines/geospatial_engine.py`)
- **Haversine Geodesic Distance** calculation in kilometers.
- **Radius-based filtering** for Registered MSMEs and Local Infrastructure POIs (Mandis, Weekly Haats, Banks, Transport Hubs).
- **Evidence Provenance & Coverage Scoring** (Section 18 & 46):
  - Classifies signals into `VERIFIED`, `DERIVED`, `ESTIMATED`, and `UNKNOWN`.
  - Disclaims registered MSME registry counts vs unregistered informal units.

---

## 📡 API Endpoints

### Opportunity Engine
- `GET  /api/intelligence/opportunity/catalog` — List all business categories.
- `POST /api/intelligence/opportunity/recommendations` — Get ranked recommendations with 7-factor fit scores.
- `POST /api/intelligence/opportunity/reverse-search` — Reverse search from assets/skills.
- `POST /api/intelligence/opportunity/score-single` — Deep breakdown for a single business.
- `POST /api/intelligence/opportunity/compare` — Side-by-side comparison matrix.

### Partner & Capability Engine
- `POST /api/intelligence/partner/gap-analysis` — 6D capability dashboard and gap detection.
- `POST /api/intelligence/partner/recommendations` — Privacy-preserving complementary partner cards.
- `POST /api/intelligence/partner/request-contact` — Mutual consent flow to reveal verified contact info.

### Geospatial Layer
- `GET  /api/intelligence/geospatial/evidence-snapshot` — Local opportunity composite and evidence coverage.
- `GET  /api/intelligence/geospatial/nearby-msmes` — Nearby registered MSMEs within radius.
- `GET  /api/intelligence/geospatial/nearby-pois` — Nearby infrastructure POIs (Mandis, Haats, Banks).
- `GET  /api/intelligence/geospatial/regional-prices` — Benchmark commodity and proxy prices.

---

## 🧪 Running Tests

```bash
cd backend
pip install -r requirements.txt
pytest -v
```
