# ThinkForge — SIH26091 Rural Business Advisory AI

## Project Specification & MVP Blueprint

**Team:** ThinkForge  
**SIH Problem Statement:** SIH26091  
**Problem:** AI-Driven Hyper-Local Business Advisory and Financial
Structuring Assistant for Rural Micro-Entrepreneurs  
**Organization:** Ministry of Social Justice and Empowerment (MoSJE)  
**Category:** Software

------------------------------------------------------------------------

## 1. Executive Summary

ThinkForge is an AI-powered rural entrepreneurship decision-support
platform. It helps a rural micro-entrepreneur understand what business
can realistically be started using their skills, capital, resources and
location; evaluates local opportunity; finds complementary partners;
tests financial viability; identifies potentially relevant government
schemes; and produces an actionable business blueprint.

The SIH91 research framing identifies two major areas: localized
feasibility analysis and financial structuring/scheme routing. The
recommended architecture is an **evidence + rules + decision system**,
not a generic LLM that writes a business plan.

The main journey is:

**Understand entrepreneur → discover opportunities → explain
recommendation → find missing capabilities/partners → simulate finances
→ match schemes → generate action plan.**

Every important result should be classified as:

- **VERIFIED** — directly supported by a source
- **DERIVED** — calculated from verified inputs
- **ESTIMATED** — model/heuristic estimate
- **UNKNOWN** — insufficient evidence

This evidence-aware approach is important because village-level market
data is incomplete.

------------------------------------------------------------------------

# 2. Problem Understanding

SIH26091 combines:

### A. Localized business feasibility

- Market reach
- Underserved niches
- Budget-scaled SWOT
- Local threats
- Competitor density
- Suggested pricing

### B. Financial structuring and scheme routing

- Project cost
- Capital requirement
- Loan planning
- EMI/repayment
- Government-scheme matching

The product should therefore behave like a **decision-support
platform**, not merely a chatbot.

------------------------------------------------------------------------

# 3. Product Vision

## Vision

**Empower rural entrepreneurs to make evidence-backed business decisions
and connect with the people, resources and financing they need to
start.**

## Product positioning

**ThinkForge — AI Rural Entrepreneurship Co-Pilot**

### Suggested tagline

> **Find the opportunity. Find the partner. Know the numbers. Start
> smarter.**

------------------------------------------------------------------------

# 4. Target Users

### Aspiring rural entrepreneur

Needs help deciding what business to start and how to begin.

### Skilled but underfunded entrepreneur

Has production/technical skills but lacks capital or market access.

### Resource-rich entrepreneur

Has capital, equipment, transport or market connections but lacks
technical/business skills.

### Future ecosystem users

Potential future users include entrepreneurship-support organizations,
facilitators and rural development programs.

------------------------------------------------------------------------

# 5. Core User Journey

## Step 1 — Smart Registration

Collect:

- Location
- Skills
- Available capital/budget
- Business interests
- Land/equipment/resources
- Experience
- Labour availability
- Risk preference
- Constraints
- Preferred language

This creates an **Entrepreneur Capability Profile**.

## Step 2 — Opportunity Discovery

Analyze:

**Skills + Capital + Resources + Location + Interests + Constraints**

and rank suitable business categories.

## Step 3 — Explainability

Show why each business received its score.

## Step 4 — Capability Gap Detection

Identify what the entrepreneur is missing:

- Capital
- Skill
- Market access
- Distribution
- Equipment
- Technology
- Management

## Step 5 — Partner Discovery

Find nearby users whose strengths complement those gaps.

## Step 6 — Financial Simulation

Test project cost, loan requirement, EMI, revenue, expenses, profit and
break-even under different scenarios.

## Step 7 — Scheme Matching

Match the entrepreneur/business profile to potentially relevant official
schemes.

## Step 8 — Business Blueprint

Generate a structured report containing evidence, assumptions,
financials, partners, scheme routes, risks and next steps.

------------------------------------------------------------------------

# 6. USP \#1 — AI Business Partner Finder

## ThinkForge’s signature differentiator

Many entrepreneurs have one side of the equation but not the other:

- Skill but no funding
- Funding but no skill
- Production capability but no market access
- Business knowledge but no distribution

ThinkForge identifies these **complementary capability gaps** and
suggests potential partners.

### Example

**User A** - Handicraft skill - ₹20,000 capital - Workspace - Limited
marketing - Handicraft interest - Nearby location

**User B** - Marketing/business skills - ₹2,00,000 capital - Market
connections - Handicraft interest - Nearby location

The system can identify:

**User A strengths + User B strengths = complementary business
capability**

### Partner Synergy Score

Example: **91/100**

Possible dimensions:

| Factor                   | Weight |
|--------------------------|-------:|
| Skill complementarity    |    30% |
| Capital compatibility    |    20% |
| Resource complementarity |    15% |
| Shared business interest |    15% |
| Location proximity       |    10% |
| Experience compatibility |    10% |

The weights should be configurable.

### Key design principle

Do not match users simply because they have similar interests.

The system should match:

> **One user’s missing capability with another user’s strength.**

### “Find What I’m Missing”

Show a capability dashboard:

``` text
Production       92%
Capital          44%
Marketing        28%
Distribution     35%
Technology       61%
Management       70%

BIGGEST GAPS
1. Market access
2. Working capital
3. Distribution
```

Then show the best complementary partners.

### Privacy

Partner discovery should initially expose only: - Approximate area -
Skills - Business interests - Investment range - Relevant resources -
Synergy score

Contact details should be shared only after mutual interest/consent.

------------------------------------------------------------------------

# 7. USP \#2 — Resource → Business Engine

Instead of:

> “What business should I start?”

ask:

> **“What can I start with what I already have?”**

Inputs:

- Skills
- Capital
- Land
- Equipment
- Raw materials
- Labour
- Existing market connections
- Location
- Interests

Output:

``` text
1. Vermicompost        91/100
2. Organic inputs      84/100
3. Food processing     76/100
```

This is a **Reverse Business Search**:

**Available resources → possible businesses**

rather than only:

**Business idea → required resources**

------------------------------------------------------------------------

# 8. USP \#3 — Explainable Business Fit Score

Instead of saying:

> “Start dairy.”

show:

### Business Fit — 87/100

### Evidence Confidence — 72/100

*Why confidence is limited:*
- Village-level demand data unavailable.
- Competitor registry coverage incomplete.
- Regional price data used as proxy.

| Factor            | Score |
|-------------------|------:|
| Capital fit       |   92% |
| Skill fit         |   88% |
| Resource fit      |   95% |
| Local opportunity |   81% |
| Market access     |   84% |
| Risk suitability  |   72% |

Then show:

### Why recommended

- Relevant skills already available
- Capital is within range
- Resources are mostly available
- Local opportunity signal is favorable

### Why not perfect

- Local demand evidence is incomplete
- Distribution capability is weak
- Competition coverage is limited

## “Why NOT This Business?”

For rejected businesses:

> Capital requirement exceeds available budget.  
> User lacks required technical skill.  
> Local registered-business density is high.  
> Reliable demand evidence is insufficient.

This makes the AI more transparent and defensible.

------------------------------------------------------------------------

# 9. USP \#4 — Business Scenario Simulator

> **Test your business before you invest.**

Allow the entrepreneur to test a business before investing.

Example:

``` text
BUSINESS SIMULATOR

Project Cost       ₹2,00,000
Own Capital          ₹80,000
Loan                ₹1,20,000
Monthly Revenue       ₹75,000
Monthly Cost          ₹52,000
Estimated Profit      ₹23,000
Break-even            11 months
Risk                  Medium
```

The user can change:

- Capital
- Selling price
- Monthly sales
- Raw material cost
- Labour cost
- Loan amount
- Interest rate
- Tenure

The dashboard immediately recalculates the outcome.

### Example

Sales -20%:

**Profit decreases → Risk increases → Break-even increases**

Loan increases:

**EMI increases → Cash-flow pressure increases**

Financial values should be calculated by deterministic code, not
invented by the LLM.

------------------------------------------------------------------------

# 10. USP \#5 — Hyper-Local Opportunity Intelligence

The system should evaluate a small geographic radius around the selected
location.

Possible signals:

- Population/household proxies
- Relevant POIs
- Registered businesses
- Business-category density
- Market accessibility
- Regional price references
- Agricultural/economic indicators
- User-provided local information

Example:

``` text
SELECTED AREA
Service radius: 5–10 km

Market signal          82%
Competition signal     64%
Price signal           78%
Resource availability  91%
Evidence coverage      71%

LOCAL OPPORTUNITY       80%
```

Do not claim that a registry is a complete census. Say:

> “11 registered enterprises found in the available registry.”

------------------------------------------------------------------------

# 11. Supporting Features

The five USPs form the core. Supporting features:

- Smart user profile
- Business idea library
- Business comparison
- Government scheme matching
- Personalized business plan
- Risk analysis
- Business recipe/action plan
- Evidence drawer
- Data coverage score
- Multilingual/simple-language mode
- Partner communication
- Report generation
- Progress tracking

------------------------------------------------------------------------

# 12. Detailed Dashboard System

The dashboard should be a major part of the MVP.

## Dashboard A — Entrepreneur Home

### KPI cards

- Profile readiness
- Available capital
- Recommended opportunities
- Potential partners
- Evidence coverage

### Visualizations

1.  **Opportunity ranking — horizontal bar chart**
2.  **Capability scorecard**
3.  **Local opportunity snapshot**
4.  **Evidence coverage**
5.  **Recommended actions**

Example:

``` text
TOP OPPORTUNITIES

Business A       █████████ 91
Business B       ████████  84
Business C       ███████   76
```

------------------------------------------------------------------------

# 13. Business Opportunity Dashboard

Selected business screen:

``` text
BUSINESS: HANDICRAFT PRODUCTS

Business Fit       89/100
Local Opportunity  84/100
Risk               Medium
Capital Required   ₹1.4L
```

Charts:

- Fit breakdown
- Cost composition
- Revenue vs cost
- Break-even
- Scenario comparison

Evidence panel:

- Source
- Date
- Coverage
- Evidence class

## Business Comparison View

Allow the entrepreneur to compare multiple opportunities side-by-side.

| Feature | Handicraft | Dairy | Food Processing |
|---|---:|---:|---:|
| **Fit Score** | 89 | 74 | 82 |
| **Capital Required** | ₹1.4L | ₹3.2L | ₹1.8L |
| **Risk** | Medium | High | Medium |
| **Local Opportunity** | 84 | 72 | 79 |
| **Skill Fit** | 94 | 48 | 77 |
| **Break-even** | 11 mo | 19 mo | 13 mo |

------------------------------------------------------------------------

# 14. Hyper-Local Map Dashboard

Map layers:

- User location
- Registered businesses
- Relevant POIs
- Markets
- Transport/access points
- Opportunity zones

Controls:

``` text
[✓] Competitors
[✓] Markets
[ ] Suppliers
[✓] Relevant POIs
[ ] Transport
```

Side panel:

``` text
Registered businesses: 11
Market signal: Medium
Price evidence: Strong
Demand evidence: Weak

Evidence coverage: 68%
```

------------------------------------------------------------------------

# 15. Business Partner Dashboard

## “Find What I’m Missing”

Capability profile:

``` text
Production       92%
Capital          44%
Marketing        28%
Distribution     35%
Technology       61%
Management       70%
```

Potential partner card:

``` text
Partner A
Skill: Marketing
Capital range: ₹1–3L
Interest: Handicrafts
Area: Nearby
Synergy: 94%

Why matched:
✓ Skill complementarity
✓ Shared interest
✓ Capital compatibility
✓ Geographic proximity

⚠ Partner not yet verified. (Verification State: BASIC)
```

------------------------------------------------------------------------

# 16. Financial Dashboard

## KPI cards

- Project cost
- Own contribution
- Required loan
- Monthly revenue
- Monthly profit
- EMI
- Break-even

## Charts

### Cost breakdown

Pie/donut chart.

### Monthly cash flow

Line chart.

### Revenue vs expenses

Line/bar chart.

### Loan repayment

Repayment table/chart.

### Scenario comparison

- Conservative
- Base
- Optimistic

------------------------------------------------------------------------

# 17. Government Scheme Dashboard & Auto-Filler

Scheme cards should show:

- Scheme name
- Potential match
- Why it matches
- Eligibility checks
- Required documents
- Official source
- Application route
- Last verified date

Never say:

> “Loan approved.”

Say:

> “Potentially suitable financing route; final approval is made by the
> authorized channel.”

------------------------------------------------------------------------

# 18. Evidence Dashboard

This is an important trust feature.

Example:

``` text
LOCAL EVIDENCE COVERAGE

Population             95%
Business registry       68%
Price data              84%
Competitor mapping      51%
Demand evidence         39%
```

Evidence classes:

**VERIFIED** — direct source  
**DERIVED** — calculated from source data  
**ESTIMATED** — model/heuristic estimate  
**UNKNOWN** — insufficient evidence

Example:

> Demand signal: Medium.  
> Evidence: population proxy + regional price references.  
> Direct village-level demand data unavailable.

------------------------------------------------------------------------

# 19. Final Business Blueprint

One-click PDF report:

1.  Entrepreneur profile
2.  Selected business
3.  Business Fit Score
4.  Local opportunity
5.  Competitor evidence
6.  Pricing evidence
7.  SWOT
8.  Risks
9.  Resource requirements
10. Partner recommendations
11. Financial structure
12. Loan/EMI
13. Scheme matches
14. Assumptions
15. Evidence coverage
16. Action plan (Task Engine)

## Action Engine (Next 7 Days)
Turn the final roadmap into concrete tasks, not generic advice.
- **Day 1** — Contact suppliers
- **Day 2** — Compare raw material prices
- **Day 3** — Talk to 5 potential customers
- **Day 4** — Connect with suggested partner
- **Day 5** — Validate selling price
- **Day 6** — Prepare financing documents
- **Day 7** — Review business viability

------------------------------------------------------------------------

# 20. UI/UX Design

## Design principles

1.  Simple first
2.  Visual before text
3.  Explain every AI recommendation
4.  Evidence one click away
5.  Progressive disclosure
6.  Mobile-first
7.  Avoid generic chatbot appearance

## Suggested navigation

``` text
🏠 Dashboard
💡 Opportunities
🤝 Partners
💰 Finance
🏛 Schemes
📍 Local Insights
📊 Reports
⚙ Profile
```

## Main dashboard

``` text
-------------------------------------------------
| Greeting                 Location     Profile |
-------------------------------------------------
| Capital | Opportunities | Partners | Readiness |
-------------------------------------------------
|         Business Opportunity Ranking           |
|                 [CHART]                         |
-------------------------------------------------
| Local Insights       | Capability Analysis     |
|      [MAP]           |       [CHART]            |
-------------------------------------------------
| Recommended Actions                           |
-------------------------------------------------
```

------------------------------------------------------------------------

# 21. Visual Design Language

Recommended direction:

- Modern dashboard
- Green/teal primary visual family
- Neutral/light background
- High contrast
- Large readable typography
- Rounded cards
- Clear status badges
- Consistent iconography

The application should feel like:

**Financial dashboard + local intelligence platform + AI advisor**

rather than a chatbot.

------------------------------------------------------------------------

# 21.5 Database Schema (Core Entities)

```text
USER
 ├── profile (name, phone, language)
 ├── skills (array of skills)
 ├── resources (array of owned assets)
 ├── interests (array of business categories)
 ├── location (lat, lng, radius)
 └── preferences (risk_tolerance)

BUSINESS
 ├── category (e.g., Dairy, Handicraft)
 ├── required_skills (array)
 ├── required_resources (array)
 ├── capital_requirement (min, max)
 ├── operating_cost (monthly estimate)
 └── revenue_model (monthly estimate)

PARTNER
 ├── user_id (FK to USER)
 ├── capabilities (array of strengths)
 ├── investment_range (min, max)
 ├── location (lat, lng)
 └── verification (status: BASIC, VERIFIED)

MATCH
 ├── user_id (FK to USER)
 ├── partner_id (FK to PARTNER)
 ├── synergy_score (0-100)
 └── reasons (JSON array of matching factors)

SCHEME
 ├── scheme_name
 ├── eligibility (JSON rules)
 ├── financial_rules (max_loan, interest, subsidy)
 ├── documents (array of required docs)
 └── source (URL/Authority)

EVIDENCE
 ├── source (e.g., e-NAM, Census)
 ├── location (lat, lng, radius)
 ├── timestamp (last fetched)
 ├── confidence (0-100)
 └── evidence_type (Price, Competitor, Demand)
```

# 21.6 API Contracts

- `POST /auth/register`
- `GET /profile`
- `GET /businesses/recommendations`
- `POST /finance/simulate`
- `GET /partners/recommendations`
- `GET /schemes/matches`

------------------------------------------------------------------------

# 22. Tech Stack

## Frontend

- Next.js / React
- Tailwind CSS
- Recharts
- MapLibre GL JS

## Backend

- Python
- FastAPI

## Database

- PostgreSQL
- PostGIS

## RAG / Vector Search

- pgvector for simpler deployment
- Qdrant as alternative

## AI

- Local Gemma model via Ollama
- LLM with structured-output prompting
- RAG for official/reference documents

## Data

- Pandas
- GeoPandas

## Financial engine

- Pure Python deterministic service

## Deployment

- Docker

------------------------------------------------------------------------

# 23. AI Architecture

Do not let the LLM control everything.

``` text
User Profile
     |
     v
Local Evidence
     |
     +-------------------+
     |                   |
     v                   v
Opportunity Engine   Financial Engine
     |                   |
     +---------+---------+
               |
               v
          Evidence Store
               |
               v
              RAG
               |
               v
              LLM
               |
               v
      Explanation + Report
```

### LLM should handle

- Explanation
- Personalization
- SWOT synthesis
- Risk explanations
- Natural-language business plans
- Multilingual/simple-language responses
- Questions over retrieved evidence

### Deterministic code should handle

- Financial totals
- EMI
- Loan amount
- Interest
- Eligibility rules
- Scheme caps
- Inspectable scoring

------------------------------------------------------------------------

# 24. Opportunity Scoring

Candidate business score can consider:

``` text
Local Demand
+ Capital Fit
+ Skill Fit
+ Resource Fit
+ Market Accessibility
+ Margin Potential
- Risk
- Competition Pressure
```

Example configurable weighting:

| Factor            | Weight |
|-------------------|-------:|
| Capital Fit       |    20% |
| Skill Fit         |    20% |
| Resource Fit      |    15% |
| Local Opportunity |    20% |
| Market Access     |    10% |
| Margin Potential  |    10% |
| Risk              |     5% |

Keep the formula inspectable and testable.

------------------------------------------------------------------------

# 25. Partner Matching Engine

``` text
User Profile
     |
     v
Identify capability gaps
     |
     v
Search users within geographic radius
     |
     v
Filter by business interest
     |
     v
Calculate complementarity
     |
     v
Calculate synergy
     |
     v
Rank candidates
     |
     v
Show top matches
```

Partner matching should be reproducible from structured data.

------------------------------------------------------------------------

# 26. Financial Engine

Inputs:

- Project cost
- Own contribution
- Loan requirement
- Interest rate
- Tenure
- Moratorium where applicable
- Operating assumptions

Outputs:

- Required financing
- EMI
- Repayment schedule
- Total interest
- Monthly cash-flow pressure
- Break-even estimate

The LLM must not determine financial numbers.

------------------------------------------------------------------------

# 27. Government Scheme Engine

Store schemes as versioned configuration.

``` json
{
  "scheme": "EXAMPLE_SCHEME",
  "effective_from": "YYYY-MM-DD",
  "project_cap": 500000,
  "loan_cap": 450000,
  "interest_rate": 0.08,
  "tenure_months": 60,
  "eligibility": [],
  "application_route": ""
}
```

Populate production rules from current official sources.

------------------------------------------------------------------------

# 28. Data Strategy

The hardest problem is likely village-level data completeness.

Store:

- Source
- Timestamp
- Geographic scope
- Coverage limitation
- Evidence class

If data is missing, the system should say so.

This creates a stronger product than pretending the data is complete.

------------------------------------------------------------------------

# 29. MVP Scope

## MVP-A — Profile

User enters: - Location - Capital - Skills - Resources - Business
interest

## MVP-B — Opportunity Engine

Support **3–5 carefully selected business categories**.

## MVP-C — Hyper-Local Evidence

Show: - Competition - Market signals - Pricing signals - Evidence
coverage

## MVP-D — Financial Structuring

Calculate: - Project cost - Own contribution - Loan - EMI - Repayment

## MVP-E — Partner Finder

Show complementary matches using: - Skills - Capital - Resources -
Interest - Location

## MVP-F — What-If Simulator

Change: - Capital - Sales - Costs - Loan - Price

## MVP-G — Evidence-Aware Report

Generate: - Recommendation - Evidence - Assumptions - Financials -
Partner - Scheme route - Action plan

------------------------------------------------------------------------

# 30. Recommended Demo Scenario

Use one strong end-to-end persona.

### Example

A rural entrepreneur:

- Handicraft skill
- ₹30,000 capital
- Workspace
- Limited market access

### Demo flow

**1. Profile**

User enters the information.

**2. Opportunity Engine**

Handicraft business receives a high fit score.

**3. Explainability**

System shows why.

**4. Capability Gap**

Marketing + capital identified as major gaps.

**5. Partner Finder**

Nearby complementary user is found.

**6. Financial Simulator**

Project cost and financing are calculated.

**7. What-if**

Sales are reduced by 20%; the system recalculates risk/profit.

**8. Scheme Matching**

Potential financing routes are displayed.

**9. Business Blueprint**

Final report is generated.

The complete story is:

**Opportunity → Partner → Finance → Action**

------------------------------------------------------------------------

# 31. Six-Person Team Structure

The project is strictly divided into 6 distinct areas of responsibility, ensuring clear separation between frontend and backend.

| Part | Member | Ownership | Key Responsibilities |
|------|--------|-----------|----------------------|
| 1 | **Madhav** | Frontend — Core UX, Auth UI & Dashboards | Next.js setup, Login/Registration UI, Entrepreneur Home Dashboard (Strictly Frontend). |
| 2 | **Harshanshu** | Frontend — Visualizations, Maps & Reporting | MapLibre integration, Recharts, Scenario Simulators, PDF generation UI. |
| 3 | **Dhruv** | Backend — Core APIs, Database & Auth Logic | PostgreSQL/PostGIS, FastAPI, Auth API, Session Management (Strictly Backend). |
| 4 | **Aishwarya** | Intelligence — Opportunity & Partner Engines | Scoring algorithms, geospatial proximity queries, capability gap logic. |
| 5 | **Kesha** | Financials — Financial Engine & Scheme Routing | Deterministic financial rules, loan calculations, scheme matching logic. |
| 6 | **Smit** | AI/Data — RAG, LLM Integration & Data Pipeline | Data ingestion (mock data for MVP), pgvector, local Gemma/Ollama prompting. |

------------------------------------------------------------------------

# 32. Development Phases

## Phase 1 — Foundation

- Database
- Authentication
- Profile
- Business categories
- Dashboard

## Phase 2 — Opportunity Engine

- Business scoring
- Comparison
- Fit score
- Explainability

## Phase 3 — Hyper-Local Layer

- Map
- Radius
- POI/business data
- Evidence panel
- Coverage score

## Phase 4 — Financial Engine

- Cost
- Loan
- EMI
- Repayment
- Simulator

## Phase 5 — Partner Finder

- Gap detection
- Nearby matching
- Synergy score
- Partner cards
- Mutual-interest flow

## Phase 6 — AI/RAG

- Evidence retrieval
- AI explanation
- SWOT
- Scheme explanations
- Report generation

## Phase 7 — Polish

- Charts
- Responsive UI
- Error handling
- Demo dataset
- Report export
- Final presentation

------------------------------------------------------------------------

# 33. Security & Privacy

Minimum requirements:

- Secure authentication
- Password hashing
- API authorization
- Input validation
- Audit logs
- No public exact addresses
- No public exact financial balances
- Mutual consent before contact sharing

Partner matching should protect users from unwanted exposure.

------------------------------------------------------------------------

# 34. AI Reliability

Bad:

> “Demand in your village is very high.”

Better:

> “Demand signal: Medium. This estimate uses population and regional
> market evidence. Direct village-level demand data is unavailable.”

When evidence is insufficient:

> **Insufficient local evidence**

This should be treated as a product feature.

------------------------------------------------------------------------

# 35. Failure Boundaries

Do not claim:

- Guaranteed business success
- Complete coverage of every rural business
- Exhaustive unregistered competitor data
- Guaranteed loan approval
- Perfect village-level demand prediction
- Exact future profit
- Guaranteed partner reliability

ThinkForge is a **decision-support system**, not a guarantee engine.

------------------------------------------------------------------------

# 36. Competitive Differentiation

### Generic AI advisor

``` text
User question
     |
     v
LLM
     |
     v
Text response
```

### ThinkForge

``` text
User Profile
     |
     v
Local Evidence
     |
     v
Opportunity Scoring
     |
     v
Capability Gap
     |
     v
Partner Matching
     |
     v
Financial Rules
     |
     v
Scheme Routing
     |
     v
RAG + LLM
     |
     v
Evidence-backed Business Blueprint
```

The key innovation is the **connection between the modules**.

------------------------------------------------------------------------

# 37. Core Innovation Story

Do not pitch the project as:

> “We use an LLM.”

Pitch it as:

> **ThinkForge combines hyper-local evidence, inspectable opportunity
> scoring, deterministic financial rules, complementary human matching
> and evidence-aware AI explanations into one rural entrepreneurship
> decision-support system.**

The product answers:

1.  **What can I start?**
2.  **Why is it suitable for me?**
3.  **What am I missing?**
4.  **Who can help me?**
5.  **Will the numbers work?**
6.  **Which financing routes may apply?**
7.  **What should I do next?**

------------------------------------------------------------------------

# 38. Future Scope

After the MVP:

- Business Pivot Engine
- Community Skill Graph
- Supplier Finder
- Customer/Market Finder
- Business progress tracking
- Verified partner profiles
- Reputation/trust layer
- Larger geographic coverage

These should remain future scope unless the core MVP is already stable.

------------------------------------------------------------------------

# 39. MVP Definition of Done

A judge should be able to enter one realistic entrepreneur profile and:

1.  View the profile.
2.  See at least 3 ranked business opportunities.
3.  Understand why the top recommendation was selected.
4.  See local evidence and coverage.
5.  Identify capability gaps.
6.  Find at least one meaningful complementary partner.
7.  View financial structure.
8.  Change a financial assumption and see results update.
9.  See potentially relevant scheme routes.
10. Generate a business blueprint.
11. Understand verified, derived, estimated and unknown values.

If these 11 steps work smoothly, the MVP tells a complete story.

------------------------------------------------------------------------

# 40. Final Product Architecture

``` text
                         THINKFORGE
                             |
              +--------------+--------------+
              |                             |
       USER PROFILE                    LOCATION
              |                             |
              +--------------+--------------+
                             |
                             v
                    LOCAL EVIDENCE LAYER
                             |
           +-----------------+-----------------+
           |                 |                 |
           v                 v                 v
    OPPORTUNITY          PARTNER           FINANCIAL
       ENGINE            ENGINE             ENGINE
           |                 |                 |
           +-----------------+-----------------+
                             |
                             v
                       SCHEME ENGINE
                             |
                             v
                       EVIDENCE STORE
                             |
                             v
                         RAG / LLM
                             |
                             v
                  EXPLANATION + REPORT
                             |
                             v
                    USER DASHBOARD
                             |
              +--------------+--------------+
              |              |              |
              v              v              v
          BUSINESS        PARTNER        FINANCIAL
          INSIGHTS         MATCH          PLAN
              |              |              |
              +--------------+--------------+
                             |
                             v
                       ACTION ROADMAP
```

------------------------------------------------------------------------

# 41. The Five Core USPs

| \#  | USP                                      | Question answered                            |
|-----|------------------------------------------|----------------------------------------------|
| 1   | **AI Business Partner Finder**           | Who can fill my capability gap?              |
| 2   | **Resource → Business Engine**           | What can I start with what I already have?   |
| 3   | **Explainable Business Fit Score**       | Why is this business suitable for me?        |
| 4   | **Business Scenario Simulator**          | Will the business work if conditions change? |
| 5   | **Hyper-Local Opportunity Intelligence** | Can this business work in my specific area?  |

## Overall journey

**Find the opportunity → understand why → find the missing
person/resources → test the numbers → identify financing routes → get an
action plan.**

------------------------------------------------------------------------

# 42. Final Pitch

> **“Rural entrepreneurs don’t always lack ideas. They often lack the
> right information, resources, connections and financial clarity to
> turn those ideas into businesses. ThinkForge brings these pieces
> together. We understand what an entrepreneur has, identify what can
> work locally, find the people who can fill the missing gaps, simulate
> whether the business is financially viable, connect the user to
> relevant schemes, and provide a clear roadmap to start.”**

------------------------------------------------------------------------

# 43. Engineering Principle

> **Use AI for reasoning, personalization and explanation; use
> deterministic systems for facts, calculations, policies and scoring.**

This gives ThinkForge better reliability, explainability, debugging and
judge-facing credibility.

The final product should feel like a **professional rural
entrepreneurship decision-support platform**, not a chatbot wrapped in a
dashboard.

------------------------------------------------------------------------

# 44. Source / Scope Note

The SIH26091 problem framing, core modules, evidence architecture,
deterministic financial-engine approach, data limitations, recommended
technology stack, MVP boundaries, dashboard concepts and six-person
implementation plan are grounded in the team’s existing SIH26091
research report.

The **AI Business Partner Finder**, its synergy scoring, and the
five-USP combination are **ThinkForge’s proposed innovation layer**
built on top of the problem statement.

Current financial/scheme rules should be verified against official
sources at implementation time and stored as versioned configuration. Do
not rely on stale static values.

------------------------------------------------------------------------

# 45. Data Acquisition Pipeline

## 1. Define what data is needed
First create a data dictionary for:
- User profile: skills, budget, resources, interests, location
- Businesses/MSMEs
- Population & demographics
- Local markets
- Nearby businesses/POIs
- Prices
- Agricultural/economic indicators
- Government schemes
- Business requirements

## 2. Identify reliable sources
Prefer official/primary sources, such as:
- Udyam/MSME data
- Census/demographic datasets
- Government scheme documents
- NSFDC/official financing information
- Geospatial/POI data
- Market/price datasets
- Agricultural/economic datasets

## 3. Collect the raw data
Get data through:
- APIs
- Downloadable datasets
- Official documents
- Structured government data
- Permitted public datasets

For every dataset, save its source, date, geographic coverage, and version.

## 4. Clean & normalize
- Remove duplicates
- Standardize names/categories
- Standardize units
- Standardize dates
- Validate locations/coordinates
- Handle missing values
- Detect obvious errors

## 5. Make the data location-aware
Use the user's location and calculate a selected radius, e.g. 5–10 km, to find relevant nearby:
- Businesses
- Markets
- Facilities
- Transport/access points
- Other local signals

## 6. Store evidence with metadata
Don't store just a number like 12 businesses.
Store something like:
- 12 registered businesses
- Source: Udyam dataset
- Area: X km radius
- Retrieved: Date
- Coverage: Registered businesses only

This is important for AI explainability and judge questions.

## 7. Generate derived data
Calculate things like:
- Business density
- Distance to market
- Nearby competitor/category count
- Capital fit
- Skill fit
- Resource fit
- Market accessibility

## 8. Feed it into the Opportunity Engine
The engine combines:
User profile + local evidence + business requirements
and calculates a Business Fit Score.

## 9. Financial data goes through a deterministic engine
For loan/financial calculations:
Project cost → Own contribution → Loan → Interest → EMI → Repayment → Profit → Break-even

The LLM should not be responsible for authoritative calculations.

## 10. AI/RAG explains the result
The verified/derived data is given to the AI so it can explain:
“Why is this business recommended?”
and generate:
- Business explanation
- SWOT
- Scheme explanation
- Business plan
- Action plan

## 11. Classify the reliability of every important output
| Type | Meaning |
|---|---|
| 🟢 VERIFIED | Directly supported by a source |
| 🔵 DERIVED | Calculated from verified data |
| 🟡 ESTIMATED | Model/heuristic estimate |
| ⚪ UNKNOWN | Not enough reliable data |

## 12. Refresh and audit
Time-sensitive data such as scheme rules, prices, and other changing information should be periodically refreshed, versioned, and logged.

**In one line:**
Collect → Clean → Geolocate → Store evidence → Derive features → Score → Financial calculation → AI explanation → Show confidence → Refresh

**The most important principle we established was:** don't let the AI invent local data. It should reason over collected evidence and clearly distinguish facts from estimates.

------------------------------------------------------------------------

# 46. Data Source → Purpose → Limitation

| Source/type | Data needed | Use | Limitation |
|---|---|---|---|
| Udyam / registered MSME data | Registered business/category/activity and geography where available | Competitor/category evidence and density | Only registered MSMEs; not a complete census. |
| Census/demographic sources | Population/household proxies | Market reach and demand proxies | May not represent current local demand. |
| Geospatial / POI data | Markets, facilities, transport/access points | Local accessibility and opportunity context | Coverage varies by area/source. |
| Market/price references | Regional/local price signals | Pricing and unit economics | May require regional proxies. |
| Agricultural/economic indicators | Relevant production/economic indicators | Opportunity/resource context | Applicability varies by business. |
| Official scheme documents / financing sources | Eligibility, caps, rates, tenure, application route | Scheme matching and financial structuring | Rules can change; version and re-check. |
| User-provided data | Skills, capital, resources, interests, constraints | Personalization and filling gaps | Treat as user input unless independently verified. |

------------------------------------------------------------------------

# 47. Critical Data Rules

- Never present incomplete registry data as a complete competitor census.
- Use wording such as “11 registered enterprises found in the available registry” rather than “11 competitors exist” unless completeness is established.
- If village-level demand is unavailable, say so and reduce confidence.
- Every important local claim should carry source, date, geographic scope and coverage information.
- Current scheme/financial parameters must be re-checked against official sources.
- The LLM must not determine authoritative financial numbers or guarantee eligibility, approval or profitability.

------------------------------------------------------------------------

# 48. Development Phases

- **Phase 1 — Foundation:** Database, authentication, profile, business categories, dashboard.
- **Phase 2 — Opportunity Engine:** Business scoring, comparison, fit score, explainability.
- **Phase 3 — Hyper-Local Layer:** Map, radius, POI/business data, evidence panel, coverage score.
- **Phase 4 — Financial Engine:** Cost, loan, EMI, repayment and simulator.
- **Phase 5 — Partner Finder:** Gap detection, nearby matching, synergy score, partner cards, mutual-interest flow.
- **Phase 6 — AI/RAG:** Evidence retrieval, AI explanation, SWOT, scheme explanations and report generation.
- **Phase 7 — Polish:** Charts, responsive UI, error handling, demo dataset, report export and final presentation.
