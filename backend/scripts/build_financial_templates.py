"""Build Financial Templates from MSME Invoices & Transactions dataset.

Usage:
    python -m scripts.build_financial_templates [--data-dir data/raw/msme_finance]

Download from: https://www.kaggle.com/datasets/kiruthikas005/msme-invoices-and-transactions
"""

import csv
import json
import os
import sys
from collections import defaultdict
from pathlib import Path
from statistics import median, mean

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


# Mapping from MSME dataset sectors to ThinkForge business category codes
SECTOR_TO_CATEGORY = {
    # Common sector names in the Kaggle dataset
    "textile": "handicraft_textiles",
    "textiles": "handicraft_textiles",
    "handicraft": "handicraft_textiles",
    "garment": "garment_tailoring_unit",
    "apparel": "garment_tailoring_unit",
    "tailoring": "garment_tailoring_unit",
    "food": "food_processing_spices",
    "food processing": "food_processing_spices",
    "spices": "food_processing_spices",
    "dairy": "dairy_micro_farm",
    "milk": "dairy_micro_farm",
    "livestock": "dairy_micro_farm",
    "organic": "organic_farm_inputs",
    "agriculture": "organic_farm_inputs",
    "farming": "organic_farm_inputs",
    "vermicompost": "vermicompost_production",
    "compost": "vermicompost_production",
    "retail": "general_retail",
    "services": "general_services",
    "manufacturing": "general_manufacturing",
    "trading": "general_trading",
}


def normalize_sector(raw_sector: str) -> str:
    """Map a raw sector name to a ThinkForge business category code."""
    s = raw_sector.strip().lower()
    for keyword, category in SECTOR_TO_CATEGORY.items():
        if keyword in s:
            return category
    return f"other_{s.replace(' ', '_')[:30]}"


def safe_float(val, default=0.0):
    """Safely parse a float from a string."""
    try:
        return float(str(val).replace(',', '').replace('₹', '').strip())
    except (ValueError, TypeError):
        return default


def load_csv_data(data_dir: str) -> list:
    """Load records from all CSV files in the data directory."""
    records = []
    data_path = Path(data_dir)
    
    if not data_path.exists():
        print(f"ERROR: Data directory not found: {data_path}")
        print(f"Download from: https://www.kaggle.com/datasets/kiruthikas005/msme-invoices-and-transactions")
        return records
    
    for csv_file in data_path.glob("*.csv"):
        print(f"  Loading CSV: {csv_file.name}")
        with open(csv_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                records.append(dict(row))
    
    print(f"  Loaded {len(records)} transaction records")
    return records


def build_templates(records: list) -> dict:
    """Aggregate transaction records into per-sector financial templates."""
    
    # Accumulate per sector
    sector_data = defaultdict(lambda: {
        "revenues": [],
        "expenses": [],
        "invoice_amounts": [],
        "payment_delays": [],
        "working_capital": [],
    })
    
    for row in records:
        # Try various column name conventions
        sector_raw = (
            row.get("sector")
            or row.get("Sector")
            or row.get("industry")
            or row.get("Industry")
            or row.get("business_type")
            or row.get("Business Type")
            or "unknown"
        )
        
        sector = normalize_sector(sector_raw)
        sd = sector_data[sector]
        
        # Revenue
        revenue = safe_float(row.get("revenue", row.get("Revenue", row.get("monthly_revenue", row.get("sales", 0)))))
        if revenue > 0:
            sd["revenues"].append(revenue)
        
        # Expenses
        expense = safe_float(row.get("expense", row.get("Expense", row.get("monthly_expense", row.get("total_expense", 0)))))
        if expense > 0:
            sd["expenses"].append(expense)
        
        # Invoice amounts
        invoice = safe_float(row.get("invoice_amount", row.get("Invoice Amount", row.get("amount", 0))))
        if invoice > 0:
            sd["invoice_amounts"].append(invoice)
        
        # Payment delay
        delay = safe_float(row.get("payment_delay", row.get("Payment Delay", row.get("delay_days", 0))))
        if delay >= 0:
            sd["payment_delays"].append(delay)
        
        # Working capital
        wc = safe_float(row.get("working_capital", row.get("Working Capital", 0)))
        if wc > 0:
            sd["working_capital"].append(wc)
    
    # Build final templates
    templates = {}
    for sector, data in sector_data.items():
        if not data["revenues"] and not data["invoice_amounts"]:
            continue
        
        med_revenue = median(data["revenues"]) if data["revenues"] else 0
        med_expense = median(data["expenses"]) if data["expenses"] else med_revenue * 0.65
        avg_delay = mean(data["payment_delays"]) if data["payment_delays"] else 0
        
        # Calculate variance for What-If scenarios
        revenue_low = med_revenue * 0.80
        revenue_high = med_revenue * 1.20
        
        # Estimate expense breakdown ratios
        total_exp = med_expense if med_expense > 0 else 1
        templates[sector] = {
            "median_monthly_revenue": round(med_revenue, 0),
            "median_monthly_expenses": round(med_expense, 0),
            "avg_working_capital_ratio": round(
                mean(data["working_capital"]) / med_revenue if med_revenue > 0 and data["working_capital"] else 0.35,
                3
            ),
            "avg_payment_delay_days": round(avg_delay, 1),
            "expense_breakdown": {
                "materials": 0.45,
                "labor": 0.30,
                "overhead": 0.25,
            },
            "revenue_variance_20pct": {
                "low": round(revenue_low, 0),
                "high": round(revenue_high, 0),
            },
            "sample_size": len(data["revenues"]),
            "median_invoice_amount": round(median(data["invoice_amounts"]), 0) if data["invoice_amounts"] else 0,
        }
    
    return templates


def main(argv=None):
    import argparse
    
    parser = argparse.ArgumentParser(description="Build financial templates from MSME transaction data")
    parser.add_argument("--data-dir", default="data/raw/msme_finance", help="Path to MSME CSV files")
    parser.add_argument("--output", default="data/financial_templates.json", help="Output JSON path")
    args, _ = parser.parse_known_args(argv)
    
    print("=" * 60)
    print("ThinkForge — MSME Financial Templates Builder")
    print("=" * 60)
    
    records = load_csv_data(args.data_dir)
    
    if not records:
        print("\nNo data found. Generating default templates from ThinkForge baselines...")
        # Fallback: generate sensible defaults from existing business catalog
        templates = {
            "handicraft_textiles": {
                "median_monthly_revenue": 45000,
                "median_monthly_expenses": 28000,
                "avg_working_capital_ratio": 0.35,
                "avg_payment_delay_days": 15,
                "expense_breakdown": {"materials": 0.50, "labor": 0.30, "overhead": 0.20},
                "revenue_variance_20pct": {"low": 36000, "high": 54000},
                "sample_size": 0,
                "median_invoice_amount": 5000,
            },
            "garment_tailoring_unit": {
                "median_monthly_revenue": 60000,
                "median_monthly_expenses": 38000,
                "avg_working_capital_ratio": 0.30,
                "avg_payment_delay_days": 10,
                "expense_breakdown": {"materials": 0.45, "labor": 0.35, "overhead": 0.20},
                "revenue_variance_20pct": {"low": 48000, "high": 72000},
                "sample_size": 0,
                "median_invoice_amount": 3500,
            },
            "food_processing_spices": {
                "median_monthly_revenue": 80000,
                "median_monthly_expenses": 52000,
                "avg_working_capital_ratio": 0.40,
                "avg_payment_delay_days": 20,
                "expense_breakdown": {"materials": 0.55, "labor": 0.25, "overhead": 0.20},
                "revenue_variance_20pct": {"low": 64000, "high": 96000},
                "sample_size": 0,
                "median_invoice_amount": 8000,
            },
            "dairy_micro_farm": {
                "median_monthly_revenue": 70000,
                "median_monthly_expenses": 45000,
                "avg_working_capital_ratio": 0.38,
                "avg_payment_delay_days": 5,
                "expense_breakdown": {"materials": 0.50, "labor": 0.28, "overhead": 0.22},
                "revenue_variance_20pct": {"low": 56000, "high": 84000},
                "sample_size": 0,
                "median_invoice_amount": 2500,
            },
            "vermicompost_production": {
                "median_monthly_revenue": 35000,
                "median_monthly_expenses": 18000,
                "avg_working_capital_ratio": 0.25,
                "avg_payment_delay_days": 12,
                "expense_breakdown": {"materials": 0.35, "labor": 0.40, "overhead": 0.25},
                "revenue_variance_20pct": {"low": 28000, "high": 42000},
                "sample_size": 0,
                "median_invoice_amount": 4000,
            },
            "organic_farm_inputs": {
                "median_monthly_revenue": 50000,
                "median_monthly_expenses": 30000,
                "avg_working_capital_ratio": 0.32,
                "avg_payment_delay_days": 18,
                "expense_breakdown": {"materials": 0.40, "labor": 0.35, "overhead": 0.25},
                "revenue_variance_20pct": {"low": 40000, "high": 60000},
                "sample_size": 0,
                "median_invoice_amount": 6000,
            },
        }
    else:
        templates = build_templates(records)
    
    # Write output
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(templates, f, indent=2, ensure_ascii=False)
    
    print(f"\n  Written {len(templates)} financial templates to: {output_path}")
    for sector, data in templates.items():
        rev = data["median_monthly_revenue"]
        exp = data["median_monthly_expenses"]
        print(f"    {sector:30s} | Revenue: ₹{rev:>8,.0f} | Expenses: ₹{exp:>8,.0f} | Margin: {((rev-exp)/rev*100) if rev > 0 else 0:.0f}%")


if __name__ == "__main__":
    main()
