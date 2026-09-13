"""
Standard Business Category Catalog for ThinkForge Opportunity Engine.
Includes Handicraft, Dairy, Food Processing, Vermicompost, Organic Inputs, and Garment/Tailoring.
"""

from typing import List, Optional, Dict
from ..models.business import BusinessCategory, BusinessRequirement
from ..models.common import RiskLevel


BUSINESS_CATALOG: Dict[str, BusinessCategory] = {
    "handicraft_textiles": BusinessCategory(
        id="handicraft_textiles",
        name="Handicraft & Textile Products",
        sector="Artisanal & Crafts",
        description="Production and supply of traditional handcrafted textiles, jute bags, home decor, and embroidery products for rural/semi-urban markets.",
        requirements=BusinessRequirement(
            required_skills=["Handicraft", "Textile Design", "Weaving", "Sewing", "Embroidery", "Crafts"],
            optional_skills=["Marketing", "Packaging", "Digital Sales"],
            required_resources=["Workspace", "Basic Tools", "Work Shed"],
            min_capital_required=25000.0,
            recommended_capital=140000.0,
            estimated_monthly_operating_cost=32000.0,
            estimated_monthly_revenue=55000.0,
            break_even_months_estimate=11,
            typical_margin_percentage=41.8,
            inherent_risk=RiskLevel.MEDIUM
        ),
        tags=["handicrafts", "textiles", "artisan", "home-based", "women-entrepreneurship"]
    ),
    
    "dairy_micro_farm": BusinessCategory(
        id="dairy_micro_farm",
        name="Micro Dairy & Milk Collection Center",
        sector="Agri-Business & Livestock",
        description="Small-scale cattle rearing, milk production, and chilled collection unit supplying local cooperatives and private dairies.",
        requirements=BusinessRequirement(
            required_skills=["Animal Husbandry", "Dairy Management", "Cattle Care", "Veterinary Basics"],
            optional_skills=["Feed Management", "Equipment Maintenance"],
            required_resources=["Cattle Shed", "Grazing Land", "Water Supply", "Power Connection"],
            min_capital_required=150000.0,
            recommended_capital=320000.0,
            estimated_monthly_operating_cost=45000.0,
            estimated_monthly_revenue=68000.0,
            break_even_months_estimate=19,
            typical_margin_percentage=33.8,
            inherent_risk=RiskLevel.HIGH
        ),
        tags=["dairy", "livestock", "milk", "agriculture", "cooperative"]
    ),
    
    "food_processing_spices": BusinessCategory(
        id="food_processing_spices",
        name="Agro-Food Processing & Spice Grinding Unit",
        sector="Food Processing",
        description="Value-added processing of local grains, lentils, flour, and spices packaging for local retail and periodic haats.",
        requirements=BusinessRequirement(
            required_skills=["Food Processing", "Grinding Mill Operation", "Quality Control", "Packaging"],
            optional_skills=["FSSAI Compliance", "Distribution", "Retail Sales"],
            required_resources=["Commercial Power", "Dry Storage Space", "Grinding Machinery"],
            min_capital_required=60000.0,
            recommended_capital=180000.0,
            estimated_monthly_operating_cost=38000.0,
            estimated_monthly_revenue=58000.0,
            break_even_months_estimate=13,
            typical_margin_percentage=34.5,
            inherent_risk=RiskLevel.MEDIUM
        ),
        tags=["food", "spices", "agro-processing", "milling", "packaging"]
    ),
    
    "vermicompost_production": BusinessCategory(
        id="vermicompost_production",
        name="Vermicompost & Bio-Fertilizer Unit",
        sector="Agri-Inputs",
        description="Organic waste conversion into high-grade vermicompost and earthworm bio-culture for local organic farming.",
        requirements=BusinessRequirement(
            required_skills=["Composting", "Organic Farming", "Bio-Fertilizer Prep"],
            optional_skills=["Bulk Transport", "B2B Sales"],
            required_resources=["Shaded Land", "Water Source", "Organic Raw Waste/Dung"],
            min_capital_required=20000.0,
            recommended_capital=85000.0,
            estimated_monthly_operating_cost=15000.0,
            estimated_monthly_revenue=32000.0,
            break_even_months_estimate=8,
            typical_margin_percentage=53.1,
            inherent_risk=RiskLevel.LOW
        ),
        tags=["vermicompost", "organic", "bio-fertilizer", "soil-health", "low-capital"]
    ),
    
    "organic_farm_inputs": BusinessCategory(
        id="organic_farm_inputs",
        name="Organic Crop Inputs & Bio-Pesticide Store",
        sector="Agri-Inputs & Retail",
        description="Production and supply of neem extracts, jeevamrut, bio-repellents, and certified organic seeds to farming clusters.",
        requirements=BusinessRequirement(
            required_skills=["Agronomy Knowledge", "Bio-Extract Preparation", "Seed Handling"],
            optional_skills=["Farmer Advisory", "Retail Management"],
            required_resources=["Storage Depot", "Packaging Setup"],
            min_capital_required=40000.0,
            recommended_capital=110000.0,
            estimated_monthly_operating_cost=22000.0,
            estimated_monthly_revenue=39000.0,
            break_even_months_estimate=10,
            typical_margin_percentage=43.6,
            inherent_risk=RiskLevel.LOW
        ),
        tags=["organic", "bio-pesticide", "seeds", "retail", "agri-retail"]
    ),
    
    "garment_tailoring_unit": BusinessCategory(
        id="garment_tailoring_unit",
        name="Custom Tailoring & Apparel Manufacturing",
        sector="Textile & Apparel",
        description="Custom tailoring, school uniform production, and bulk garment batch stitching for local institutions and retailers.",
        requirements=BusinessRequirement(
            required_skills=["Tailoring", "Stitching", "Pattern Cutting", "Garment Finishing"],
            optional_skills=["Machine Maintenance", "Bulk Sourcing"],
            required_resources=["Sewing Machines", "Work Space", "Power Connection"],
            min_capital_required=30000.0,
            recommended_capital=95000.0,
            estimated_monthly_operating_cost=20000.0,
            estimated_monthly_revenue=36000.0,
            break_even_months_estimate=9,
            typical_margin_percentage=44.4,
            inherent_risk=RiskLevel.LOW
        ),
        tags=["tailoring", "garments", "stitching", "uniforms", "micro-enterprise"]
    ),

}

def get_all_businesses() -> List[BusinessCategory]:
    return list(BUSINESS_CATALOG.values())


def get_business_by_id(business_id: str) -> Optional[BusinessCategory]:
    return BUSINESS_CATALOG.get(business_id)
