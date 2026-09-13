"""Ingest Indian Government Schemes from Kaggle CSV/JSON into PostgreSQL.

Usage:
    python -m scripts.ingest_schemes [--dry-run] [--data-dir backend/data/raw/schemes]

Downloads from: https://www.kaggle.com/datasets/jainamgada45/indian-government-schemes
Expected files in data-dir: CSV or JSON files with scheme records.
"""

import csv
import json
import os
import re
import sys
from pathlib import Path

# Add parent to path so we can import app modules
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_sessionmaker, get_engine, Base
from app.models.scheme import GovernmentScheme


# --- Amount Extraction ---
AMOUNT_PATTERNS = [
    (r'₹?\s*(\d+(?:\.\d+)?)\s*(?:crore|cr)', 1e7),       # crore
    (r'₹?\s*(\d+(?:\.\d+)?)\s*(?:lakh|lac|lakhs)', 1e5),  # lakh
    (r'₹?\s*(\d+(?:,\d+)*(?:\.\d+)?)', 1),                # raw number
]

def extract_amount(text: str) -> float:
    """Extract monetary amount from text like 'up to ₹50 Lakhs' -> 5000000."""
    if not text:
        return 0.0
    text_lower = text.lower()
    for pattern, multiplier in AMOUNT_PATTERNS:
        match = re.search(pattern, text_lower)
        if match:
            num_str = match.group(1).replace(',', '')
            return float(num_str) * multiplier
    return 0.0


def extract_interest_rate(text: str) -> float:
    """Extract interest rate from text like '8.5%' -> 0.085."""
    if not text:
        return 0.085  # default
    match = re.search(r'(\d+(?:\.\d+)?)\s*%', str(text))
    if match:
        return float(match.group(1)) / 100.0
    return 0.085


def extract_subsidy_pct(text: str) -> float:
    """Extract subsidy percentage from text like '35% subsidy' -> 0.35."""
    if not text:
        return 0.0
    match = re.search(r'(\d+(?:\.\d+)?)\s*%', str(text))
    if match:
        return float(match.group(1)) / 100.0
    return 0.0


def categorize_scheme(name: str, details: str) -> list:
    """Auto-tag scheme categories based on name and description keywords."""
    text = f"{name} {details}".lower()
    tags = []
    
    keyword_map = {
        "agriculture": ["agriculture", "farming", "kisan", "krishi", "crop", "agri"],
        "msme": ["msme", "micro", "small", "medium", "enterprise", "udyam", "mudra"],
        "women": ["women", "mahila", "female", "lady", "girl"],
        "sc_st": ["sc", "st", "scheduled caste", "scheduled tribe", "obc", "backward"],
        "food_processing": ["food", "processing", "fssai", "dairy", "milk"],
        "handicraft": ["handicraft", "artisan", "handloom", "weaver", "craft", "textile"],
        "education": ["education", "skill", "training", "scholarship"],
        "health": ["health", "medical", "hospital", "ayush"],
        "housing": ["housing", "awas", "shelter", "home"],
        "finance": ["loan", "credit", "subsidy", "bank", "finance", "capital"],
        "rural": ["rural", "gram", "village", "panchayat"],
        "startup": ["startup", "incubat", "entrepreneur", "innovation"],
    }
    
    for tag, keywords in keyword_map.items():
        if any(kw in text for kw in keywords):
            tags.append(tag)
    
    return tags if tags else ["general"]


def determine_scheme_level(row: dict) -> tuple:
    """Determine if scheme is CENTRAL or STATE, and extract state if applicable."""
    # Check various possible column names
    for key in ["level", "scheme_level", "type", "scheme_type"]:
        val = row.get(key, "").strip().lower()
        if "state" in val:
            state_name = row.get("state", row.get("state_name", ""))
            return "STATE", state_name or None
        if "central" in val:
            return "CENTRAL", None
    
    # Check scheme name for state indicators
    name = row.get("scheme_name", row.get("schemeName", "")).lower()
    gujarat_keywords = ["gujarat", "gj", "gandhinagar"]
    if any(kw in name for kw in gujarat_keywords):
        return "STATE", "Gujarat"
    
    return "CENTRAL", None


def parse_documents_required(text: str) -> list:
    """Parse documents from text into a list."""
    if not text:
        return ["Aadhaar Card", "Bank Account"]
    if isinstance(text, list):
        return text
    # Split by common delimiters
    docs = re.split(r'[,;\n•·]', text)
    return [d.strip() for d in docs if d.strip()]


def row_to_scheme_dict(row: dict) -> dict:
    """Convert a raw CSV/JSON row into a GovernmentScheme-compatible dict."""
    # Handle different column name conventions from Kaggle datasets
    name = (
        row.get("scheme_name")
        or row.get("schemeName")
        or row.get("Scheme Name")
        or row.get("title")
        or row.get("name")
        or "Unknown Scheme"
    )
    
    description = (
        row.get("details")
        or row.get("description")
        or row.get("Description")
        or row.get("about")
        or ""
    )
    
    benefits = (
        row.get("benefits")
        or row.get("Benefits")
        or row.get("benefits_text")
        or ""
    )
    
    eligibility_text = (
        row.get("eligibility")
        or row.get("Eligibility")
        or row.get("eligibility_criteria")
        or ""
    )
    
    documents_text = (
        row.get("documents_required")
        or row.get("Documents Required")
        or row.get("documents")
        or ""
    )
    
    # Build eligibility rules JSON
    eligibility_rules = {}
    if eligibility_text:
        eligibility_rules["raw_text"] = str(eligibility_text)[:2000]
        if "18" in str(eligibility_text):
            eligibility_rules["min_age"] = 18
    
    # Extract amounts
    max_loan = extract_amount(str(row.get("loan_limit", row.get("max_amount", ""))))
    if max_loan == 0:
        max_loan = extract_amount(description)
    if max_loan == 0:
        max_loan = 500000  # default ₹5L
    
    interest_rate = extract_interest_rate(str(row.get("interest_rate", "")))
    subsidy_pct = extract_subsidy_pct(str(row.get("subsidy", row.get("subsidy_percent", ""))))
    
    # Generate short_code from name
    words = re.findall(r'[A-Z]{2,}', name)
    short_code = words[0] if words else name[:10].upper().replace(' ', '_')
    # Ensure uniqueness by appending hash
    short_code = f"{short_code}_{abs(hash(name)) % 10000}"
    
    scheme_level, target_state = determine_scheme_level(row)
    category_tags = categorize_scheme(name, description)
    
    official_url = (
        row.get("official_source_url")
        or row.get("url")
        or row.get("link")
        or row.get("application_url")
        or None
    )
    
    authority = (
        row.get("authority_name")
        or row.get("ministry")
        or row.get("Ministry")
        or row.get("department")
        or "Government of India"
    )
    
    return {
        "scheme_name": name[:150],
        "short_code": short_code[:50],
        "description": (description or benefits or "No description available")[:5000],
        "eligibility_rules": eligibility_rules,
        "max_loan_amount": int(max_loan),
        "interest_rate_annual": interest_rate,
        "subsidy_percentage": subsidy_pct,
        "tenure_months_max": 60,
        "required_documents": parse_documents_required(documents_text),
        "official_source_url": str(official_url)[:255] if official_url else None,
        "authority_name": str(authority)[:100],
        "is_active": True,
        "scheme_level": scheme_level,
        "target_state": target_state,
        "category_tags": category_tags,
        "benefits_text": str(benefits)[:5000] if benefits else None,
    }


def load_raw_data(data_dir: str) -> list:
    """Load scheme records from CSV or JSON files in the data directory."""
    records = []
    data_path = Path(data_dir)
    
    if not data_path.exists():
        print(f"ERROR: Data directory not found: {data_path}")
        print(f"Please download the dataset from:")
        print(f"  https://www.kaggle.com/datasets/jainamgada45/indian-government-schemes")
        print(f"And extract it to: {data_path}")
        return records
    
    # Try JSON files
    for json_file in data_path.glob("*.json"):
        print(f"  Loading JSON: {json_file.name}")
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                records.extend(data)
            elif isinstance(data, dict):
                records.append(data)
    
    # Try CSV files
    for csv_file in data_path.glob("*.csv"):
        print(f"  Loading CSV: {csv_file.name}")
        with open(csv_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                records.append(dict(row))
    
    print(f"  Loaded {len(records)} raw scheme records")
    return records


async def ingest_schemes(data_dir: str, dry_run: bool = False):
    """Main ingestion function."""
    print("=" * 60)
    print("ThinkForge — Government Schemes Ingestion")
    print("=" * 60)
    
    raw_records = load_raw_data(data_dir)
    if not raw_records:
        print("  No Kaggle scheme files found in data_dir. Seeding foundational Central & Gujarat schemes...")
        raw_records = [
            {
                "scheme_name": "Prime Minister Employment Generation Programme",
                "short_code": "PMEGP",
                "details": "Credit-linked subsidy programme aiming to generate self-employment opportunities through micro-enterprise ventures in rural and urban areas.",
                "benefits": "Up to 35% capital subsidy in rural areas. Project cost up to ₹50 Lakhs for manufacturing and ₹20 Lakhs for services.",
                "eligibility": "Age 18+, minimum 8th standard pass for projects over 10 Lakhs in manufacturing. Rural beneficiaries receive 35% subsidy (special category).",
                "documents": "Aadhaar, Project Report, EDP Training Certificate, Caste/Category Certificate, Rural Area Certificate",
                "level": "CENTRAL",
                "state": None,
                "loan_limit": "50 Lakhs",
                "subsidy": "35%",
                "interest_rate": "8.5%",
                "authority": "Ministry of MSME / KVIC",
                "url": "https://www.kviconline.gov.in/pmegpeportal",
                "category_tags": ["msme", "finance", "rural", "manufacturing", "services"],
            },
            {
                "scheme_name": "Pradhan Mantri MUDRA Yojana",
                "short_code": "MUDRA",
                "details": "Collateral-free institutional credit to non-corporate, non-farm small/micro enterprises up to ₹10 Lakhs (Shishu up to 50k, Kishore up to 5L, Tarun up to 10L).",
                "benefits": "Zero collateral, affordable interest rate, flexible repayment up to 5 years.",
                "eligibility": "Any Indian citizen with a viable business plan for a non-farm income-generating activity such as manufacturing, processing, trading, or service sector.",
                "documents": "Aadhaar, PAN, Proof of business address, Quotation of machinery/items, Bank statement",
                "level": "CENTRAL",
                "state": None,
                "loan_limit": "10 Lakhs",
                "subsidy": "0%",
                "interest_rate": "9.0%",
                "authority": "Department of Financial Services / MUDRA",
                "url": "https://www.mudra.org.in",
                "category_tags": ["msme", "finance", "handicraft", "women", "startup"],
            },
            {
                "scheme_name": "Stand-Up India Scheme",
                "short_code": "STAND_UP_INDIA",
                "details": "Facilitates bank loans between ₹10 Lakhs and ₹1 Crore to at least one SC/ST borrower and at least one woman borrower per bank branch for setting up a greenfield enterprise.",
                "benefits": "Composite loan up to 85% of the project cost covering term loan and working capital.",
                "eligibility": "SC/ST and/or women entrepreneurs above 18 years of age. Enterprise must be a greenfield project in manufacturing, services, agri-allied, or trading sector.",
                "documents": "Identity proof, Caste certificate (if SC/ST), Project report, Pollution control clearance, Partnership deed/Incorporation",
                "level": "CENTRAL",
                "state": None,
                "loan_limit": "1 Crore",
                "subsidy": "15%",
                "interest_rate": "8.25%",
                "authority": "SIDBI / Ministry of Finance",
                "url": "https://www.standupmitra.in",
                "category_tags": ["finance", "women", "sc_st", "msme", "startup"],
            },
            {
                "scheme_name": "PM Formalisation of Micro food processing Enterprises Scheme",
                "short_code": "PMFME",
                "details": "Centrally sponsored scheme to enhance the competitiveness of existing individual micro-enterprises in the unorganized segment of the food processing industry.",
                "benefits": "Credit-linked capital subsidy at 35% of the eligible project cost with a maximum ceiling of ₹10 Lakhs per unit.",
                "eligibility": "Existing or new micro food processing units, FPOs, SHGs, and producer cooperatives.",
                "documents": "Aadhaar, FSSAI registration/undertaking, Bank statement, Electricity bill, Project report",
                "level": "CENTRAL",
                "state": None,
                "loan_limit": "10 Lakhs",
                "subsidy": "35%",
                "interest_rate": "8.75%",
                "authority": "Ministry of Food Processing Industries (MoFPI)",
                "url": "https://pmfme.mofpi.gov.in",
                "category_tags": ["food_processing", "agriculture", "finance", "msme", "rural"],
            },
            {
                "scheme_name": "Gujarat Industrial Policy — Assistance to Micro Enterprises",
                "short_code": "GJ_MSME_CAP_SUB",
                "details": "Capital investment subsidy for new micro enterprises established in Gujarat under the Gujarat Industrial Policy.",
                "benefits": "Capital subsidy of 25% of eligible fixed capital investment up to ₹35 Lakhs in Category 1 talukas, 20% up to ₹30 Lakhs in Category 2, and 10% in Category 3.",
                "eligibility": "Micro enterprises registered under Udyam in Gujarat engaged in manufacturing activities.",
                "documents": "Udyam Registration, Electricity connection, Machinery invoices, Chartered Accountant certificate, Gujarat domicile",
                "level": "STATE",
                "state": "Gujarat",
                "loan_limit": "35 Lakhs",
                "subsidy": "25%",
                "interest_rate": "7.5%",
                "authority": "Industries Commissionerate, Government of Gujarat",
                "url": "https://ic.gujarat.gov.in",
                "category_tags": ["msme", "finance", "manufacturing", "rural"],
            },
            {
                "scheme_name": "Jyoti Gramodhyog Vikas Yojana (JGVY)",
                "short_code": "JGVY",
                "details": "Gujarat state scheme to encourage self-employment in rural areas by establishing cottage and village industries.",
                "benefits": "Margin money subsidy up to 25% for general category and up to 30% for SC/ST/SEBC/Women/Physically Handicapped beneficiaries.",
                "eligibility": "Rural residents of Gujarat aged 25 to 50 years with basic education and local residency certificate.",
                "documents": "Ration Card, School Leaving Certificate, Gram Panchayat NOC, Income Certificate, Project Profile",
                "level": "STATE",
                "state": "Gujarat",
                "loan_limit": "25 Lakhs",
                "subsidy": "30%",
                "interest_rate": "8.0%",
                "authority": "Gujarat Cottage Industries & Khadi Board",
                "url": "https://cottage.gujarat.gov.in",
                "category_tags": ["rural", "handicraft", "women", "msme", "finance"],
            },
            {
                "scheme_name": "Mukhyamantri Mahila Utkarsh Yojana (MMUY)",
                "short_code": "MMUY",
                "details": "Gujarat state initiative providing interest-free loans of ₹1 Lakh to women Self Help Groups (Joint Liability Groups) for starting micro-enterprises.",
                "benefits": "Interest-free loan (0% interest to women SHG, government pays the interest subsidy directly to banks).",
                "eligibility": "Women Joint Liability and Earning Groups (JLEG) comprising 10 women in rural or urban Gujarat.",
                "documents": "Group resolution, Aadhaar of all members, SHG bank account passbook, Gujarat residence proof",
                "level": "STATE",
                "state": "Gujarat",
                "loan_limit": "1 Lakh",
                "subsidy": "100% interest subsidy",
                "interest_rate": "0.0%",
                "authority": "Gujarat Livelihood Promotion Company (GLPC)",
                "url": "https://glpc.gujarat.gov.in",
                "category_tags": ["women", "rural", "finance", "handicraft"],
            },
            {
                "scheme_name": "Scheme of Fund for Regeneration of Traditional Industries (SFURTI)",
                "short_code": "SFURTI",
                "details": "Cluster-based development scheme to make traditional industries (artisans, bamboo, honey, khadi) more productive and competitive.",
                "benefits": "Financial support up to ₹2.5 Crore for Regular Clusters (up to 500 artisans) and up to ₹5 Crore for Major Clusters.",
                "eligibility": "Artisan clusters, NGOs, SHGs, and Panchayati Raj Institutions representing rural artisans.",
                "documents": "Cluster Diagnostic Study, Detailed Project Report, Artisan enrollment records",
                "level": "CENTRAL",
                "state": None,
                "loan_limit": "2.5 Crore",
                "subsidy": "90%",
                "interest_rate": "0.0%",
                "authority": "Ministry of MSME",
                "url": "https://sfurti.msme.gov.in",
                "category_tags": ["handicraft", "rural", "finance", "msme"],
            },
        ]
    
    # Convert to scheme dicts
    scheme_dicts = []
    seen_names = set()
    for row in raw_records:
        try:
            d = row_to_scheme_dict(row)
            if d["scheme_name"] not in seen_names:
                seen_names.add(d["scheme_name"])
                scheme_dicts.append(d)
        except Exception as e:
            print(f"  WARN: Skipping row: {e}")
    
    print(f"  Parsed {len(scheme_dicts)} unique schemes")
    
    if dry_run:
        print("\n--- DRY RUN (no DB writes) ---")
        for i, s in enumerate(scheme_dicts[:10]):
            print(f"  [{i+1}] {s['scheme_name']} | {s['scheme_level']} | tags={s['category_tags']}")
        print(f"  ... and {len(scheme_dicts) - 10} more")
        return
    
    # Insert into database
    engine = get_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    sessionmaker = get_sessionmaker()
    async with sessionmaker() as db:
        inserted = 0
        skipped = 0
        for s_dict in scheme_dicts:
            existing = await db.execute(
                select(GovernmentScheme).where(
                    GovernmentScheme.scheme_name == s_dict["scheme_name"]
                )
            )
            if existing.scalar_one_or_none():
                skipped += 1
                continue
            
            scheme = GovernmentScheme(**s_dict)
            db.add(scheme)
            inserted += 1
        
        await db.commit()
        print(f"\n  DONE: Inserted {inserted} schemes, skipped {skipped} duplicates")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Ingest government schemes into ThinkForge DB")
    parser.add_argument("--dry-run", action="store_true", help="Parse and validate without writing to DB")
    parser.add_argument("--data-dir", default="data/raw/schemes", help="Path to raw scheme data files")
    args = parser.parse_args()
    
    asyncio.run(ingest_schemes(args.data_dir, dry_run=args.dry_run))
