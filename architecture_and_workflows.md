# ThinkForge — Comprehensive Architecture, Workflows, and Roles

This document outlines the entire technical structure of the ThinkForge platform, including detailed features, APIs, database models, and the breakdown of responsibilities per team member based on the 6-person structure.

---

## Part 1: Frontend — Core UX, Auth UI & Dashboards
**Assigned to: Madhav**

### Tech Stack
* **Language:** TypeScript / JavaScript *(For strongly-typed frontend development ensuring robust UI components).*
* **Framework:** Next.js / React *(For building the single-page application, handling client-side routing, and rendering the interactive dashboards).*
* **Styling:** Tailwind CSS *(For rapid, responsive, and consistent UI styling without writing custom CSS files).*

### Responsibilities
* Setup and architecture of the Next.js application.
* Design and implementation of the Login and Registration UI flows.
* Build the Entrepreneur Home Dashboard (the main landing interface post-login).
* Ensure strict adherence to frontend-only logic (no direct DB calls).

### Detailed Features
* **Smart Registration UI:** The frontend forms that securely collect an entrepreneur's capabilities (skills, capital, land, risk appetite) and communicate with backend auth and profile APIs.
* **Home Dashboard:** Displays KPI cards (Profile readiness, Available capital, recommended opportunities) and integrates data fetched from the backend.

---

## Part 2: Frontend — Visualizations, Maps & Reporting
**Assigned to: Harshanshu**

### Tech Stack
* **Language:** TypeScript / JavaScript *(For writing client-side logic and managing map states).*
* **Framework:** Next.js / React *(For building the UI components that host the maps and charts).*
* **Libraries:** Recharts *(Used to render the financial charts in the Business Scenario Simulator)*, MapLibre GL JS *(Used to render the interactive Hyper-Local Map and plot geospatial data like POIs and competitors).*

### Responsibilities
* Integrate mapping libraries (MapLibre GL JS) for geospatial data display.
* Create interactive data visualizations using Recharts.
* Implement the UI for Scenario Simulators and PDF report generation.

### Detailed Features
* **Hyper-Local Map Dashboard:** Visual interface displaying layers like user location, registered businesses, and POIs over a map.
* **Business Scenario Simulator UI:** Interactive interface where users can tweak inputs (capital, loan, price) and instantly see recalculated metrics via charts (donut, line charts).
* **Business Blueprint Generation:** A one-click PDF export feature that synthesizes evidence, financials, and action items into a clean, printable report.

---

## Part 3: Backend — Core APIs, Database & Auth Logic
**Assigned to: Dhruv**

### Tech Stack
* **Language:** Python 3 *(For writing the backend business logic and API endpoints).*
* **Framework:** FastAPI *(For building high-performance, asynchronous REST APIs used by the frontend).*
* **Database:** PostgreSQL with PostGIS *(PostgreSQL stores all user profiles and relational data. PostGIS is an extension that allows the database to perform spatial queries, like finding nearby users or resources).*
* **ORM / Tools:** SQLAlchemy (asyncpg/psycopg2) *(For interacting with the database using Python objects)*, Docker *(For containerizing the backend and database for consistent cross-platform deployment).*

### Responsibilities
* Establish the core FastAPI backend and route structure.
* Design and implement robust API endpoints for Authentication and Profiles.
* Manage the PostgreSQL/PostGIS database, session management, and JWT-based secure authentication.

### APIs & Models Managed
* **Auth APIs (`/auth`):** `POST /register`, `POST /login`, `POST /refresh`, `GET /me`.
* **Profile APIs (`/profile`):** Handle CRUD operations for user profiles, skills, and resources.
* **Database Models:** `User`, `Profile`, `Skill`, `UserSkill`, `Resource`, `UserResource`, `AuditLog`.

---

## Part 4: Intelligence — Opportunity & Partner Engines
**Assigned to: Aishwarya**

### Tech Stack
* **Language:** Python 3 *(For writing the matching algorithms and scoring logic).*
* **Database:** PostGIS (Geospatial queries) *(Used to execute radius-based searches to find complementary partners and local market data).*
* **Libraries:** Pandas, GeoPandas *(Used for complex data manipulation, calculating synergy scores, and processing geographical data arrays).*

### Responsibilities
* Develop the core logic and algorithms for business opportunity scoring and partner matching.
* Execute geospatial proximity queries utilizing PostGIS.
* Identify capability gaps (e.g., has land but lacks capital) and match users.

### Detailed Features & APIs
* **Opportunity Discovery & Reverse Business Search:** Analyzes entrepreneur capabilities against business templates to generate an explainable "Business Fit Score."
* **Partner Match Engine:** Geographically queries the database to find complementary nearby partners and calculates a "Synergy Score."
* **APIs:** `GET /businesses/recommendations`, `GET /partners/recommendations`.
* **Models:** `BusinessCategoryModel`, `PartnerProfileModel`, `PartnerMatch`.

---

## Part 5: Financials — Financial Engine & Scheme Routing
**Assigned to: Kesha**

### Tech Stack
* **Language:** Python 3 (Pure deterministic rules/logic) *(Used to write the strict mathematical functions that calculate EMIs, loan repayment schedules, and financial totals without hallucination risks from AI).*
* **Framework:** FastAPI (Endpoint integration) *(Used to expose the financial engine's calculations as accessible API endpoints for the frontend simulator).*

### Responsibilities
* Build deterministic financial rules and loan calculation logic (EMI, repayment schedules).
* Implement the scheme matching logic based on the user's profile and business scale.

### Detailed Features & APIs
* **Deterministic Financial Engine:** Processes simulator inputs and outputs exact financial metrics without relying on LLM estimations.
* **Scheme Matching Engine:** Compares project costs and user profiles with a configured database of government schemes.
* **APIs:** `POST /finance/simulate`, `GET /schemes/matches`.
* **Models:** `GovernmentScheme`, and in-memory calculation models like `SimulatorInput`, `SimulatorOutput`.

---

## Part 6: AI/Data — RAG, LLM Integration & Data Pipeline
**Assigned to: Smit**

### Tech Stack
* **Language:** Python 3 *(For scripting the data pipelines and integrating LLM APIs).*
* **AI/LLM:** Local Gemma model via Ollama *(Used to generate natural-language explanations of the Business Fit Score and synthesize the final Business Blueprint without relying solely on external, paid APIs).*
* **Database:** pgvector / Qdrant *(Vector database used for Retrieval-Augmented Generation to quickly search and retrieve relevant government scheme documents and official data).*
* **Libraries:** Pandas, GeoPandas *(Used for cleaning, normalizing, and ingesting raw datasets into the database).*

### Responsibilities
* Set up data ingestion pipelines and manage hyper-local evidence data (competitors, POIs).
* Implement Vector Search (using pgvector or Qdrant) for official document retrieval.
* Integrate the Local Gemma model via Ollama for RAG (Retrieval-Augmented Generation) and structured-output prompting.

### Detailed Features & APIs
* **Hyper-Local Opportunity Intelligence:** Sources and stores local data signals, returning opportunity metrics based on density and population proxies.
* **Evidence-Aware AI Explanations:** Uses LLMs exclusively for explaining SWOT, reasoning recommendations, and generating natural-language business plans—never for calculating deterministic financials.
* **APIs:** `GET /evidence/nearby`.
* **Models:** `EvidenceRecord`.

---

## Complete End-to-End Workflow: How ThinkForge Works

ThinkForge operates on a seamless, linear journey: **Opportunity → Partner → Finance → Action**. 
Here is a step-by-step breakdown of exactly how a rural entrepreneur interacts with the platform from start to finish:

### 1. Smart Profile Creation (The Foundation)
The journey begins with the entrepreneur entering their details into the **Frontend UI**. They input their geographic location, available capital, existing skills, owned resources (like land or a tractor), and risk tolerance. This creates a highly personalized "Entrepreneur Capability Profile" in the **Backend Database**.

### 2. Opportunity Engine (Reverse Business Search)
Instead of asking the user for a business idea, the **Opportunity Engine** asks: *"What can you start with what you already have?"* It cross-references the user's profile against a library of business templates and calculates a **Business Fit Score**. The system outputs the top 3-5 recommended business categories (e.g., Handicrafts, Dairy, Vermicompost).

### 3. Hyper-Local Evidence & Explainability
For the chosen business, the **Local Evidence Layer** scans a 5–10km radius using PostGIS. It checks competitor density, market access, and demographic proxies. The AI then explains *exactly why* this business was recommended (e.g., "You have 90% of the required capital and strong market access, but lack marketing skills").

### 4. Capability Gap Detection & Partner Match
The **Intelligence Engine** identifies exactly what the entrepreneur is missing to succeed (e.g., they have the production skill but lack capital and marketing). It performs a geographic search to find another nearby user who has those exact missing traits. A **Synergy Score** is generated, and a complementary business partner is recommended.

### 5. Financial Simulator & What-If Scenarios
With the business and partner identified, the user enters the **Financial Simulator**. The **Deterministic Financial Engine** calculates the exact project cost, EMI, and break-even point. The user can tweak variables (e.g., "What if sales drop by 20%? What if I take a smaller loan?") and watch the charts and risk levels instantly recalculate.

### 6. Government Scheme Matching
Based on the finalized project cost and the user's demographic profile, the **Scheme Engine** scans a database of active government schemes. It recommends the best financing routes (e.g., mudra loans, subsidies) and lists the eligibility criteria.

### 7. The Final Business Blueprint (Action Plan)
Finally, all this data—the chosen business, local evidence, financial projections, matched partner, and scheme routes—is fed into the **RAG/LLM Pipeline**. The AI synthesizes everything into an easy-to-read, printable **Business Blueprint PDF**. Most importantly, it generates a concrete **7-Day Action Roadmap** (e.g., "Day 1: Call this supplier. Day 2: Meet with recommended partner.") so the entrepreneur knows exactly what to do next.
