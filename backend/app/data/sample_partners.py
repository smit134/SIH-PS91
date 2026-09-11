"""
Sample Partner Database for ThinkForge Partner Synergy & Proximity Matching Engine.
Includes diverse partners with complementary capital, skills, transport, and resources.
"""

from typing import List
from ..models.partner import PartnerProfile
from ..models.user import LocationPoint
from ..models.common import VerificationState


SAMPLE_PARTNERS: List[PartnerProfile] = [
    PartnerProfile(
        partner_id="partner_mkt_01",
        name="Ramesh Verma",
        phone="+91-98765-43210",
        location=LocationPoint(
            latitude=28.6145,
            longitude=77.2100,
            village_or_town="District Market Town",
            district="Central District",
            state="Demo State",
            service_radius_km=15.0
        ),
        capabilities=["Marketing", "Capital", "Distribution", "Management"],
        skills=["Digital Marketing", "Wholesale Sales", "Buyer Negotiation", "Accounting"],
        resources=["Commercial Shop Front", "Delivery Van", "Retail Contacts"],
        investment_min=100000.0,
        investment_max=300000.0,
        experience_years=6.0,
        business_interests=["handicraft_textiles", "food_processing_spices", "garment_tailoring_unit"],
        verification_state=VerificationState.VERIFIED
    ),
    
    PartnerProfile(
        partner_id="partner_tech_02",
        name="Pooja Sharma",
        phone="+91-98123-45678",
        location=LocationPoint(
            latitude=28.6250,
            longitude=77.2250,
            village_or_town="North Block Center",
            district="Central District",
            state="Demo State",
            service_radius_km=10.0
        ),
        capabilities=["Technology", "Production", "Quality Control"],
        skills=["Machine Maintenance", "Computerized Pattern Cutting", "Packaging Quality"],
        resources=["Heavy Duty Sewing Machine", "Packaging Sealer", "Computer"],
        investment_min=40000.0,
        investment_max=120000.0,
        experience_years=4.0,
        business_interests=["handicraft_textiles", "garment_tailoring_unit"],
        verification_state=VerificationState.BASIC
    ),
    
    PartnerProfile(
        partner_id="partner_agri_03",
        name="Kailash Patel",
        phone="+91-97234-56789",
        location=LocationPoint(
            latitude=28.5800,
            longitude=77.1900,
            village_or_town="Green Valley Village",
            district="Central District",
            state="Demo State",
            service_radius_km=20.0
        ),
        capabilities=["Distribution", "Raw Materials", "Production"],
        skills=["Organic Farming", "Bio-Fertilizer Prep", "Tractor Driving"],
        resources=["1.5 Acre Farmland", "Tractor & Trolley", "Cattle Shed"],
        investment_min=50000.0,
        investment_max=150000.0,
        experience_years=8.0,
        business_interests=["vermicompost_production", "organic_farm_inputs", "dairy_micro_farm"],
        verification_state=VerificationState.VERIFIED
    ),

    PartnerProfile(
        partner_id="partner_dairy_04",
        name="Sunita Yadav",
        phone="+91-96543-21098",
        location=LocationPoint(
            latitude=28.6300,
            longitude=77.1800,
            village_or_town="Milk Producers Hub",
            district="Central District",
            state="Demo State",
            service_radius_km=12.0
        ),
        capabilities=["Capital", "Management", "Marketing"],
        skills=["Dairy Cooperative Management", "Bulk Chilling Operation", "Accounting"],
        resources=["Chilled Milk Storage", "DG Power Backup"],
        investment_min=150000.0,
        investment_max=400000.0,
        experience_years=5.0,
        business_interests=["dairy_micro_farm", "food_processing_spices"],
        verification_state=VerificationState.VERIFIED
    ),

    PartnerProfile(
        partner_id="partner_logistics_05",
        name="Anil Kumar",
        phone="+91-95432-10987",
        location=LocationPoint(
            latitude=28.6400,
            longitude=77.2500,
            village_or_town="Railway Junction Block",
            district="Central District",
            state="Demo State",
            service_radius_km=25.0
        ),
        capabilities=["Distribution", "Logistics", "Transport"],
        skills=["Route Planning", "Freight Handling", "Fleet Operations"],
        resources=["Pick-up Auto Truck", "Warehouse Bay"],
        investment_min=30000.0,
        investment_max=80000.0,
        experience_years=7.0,
        business_interests=["handicraft_textiles", "food_processing_spices", "vermicompost_production"],
        verification_state=VerificationState.BASIC
    )
]
