"""
Sample Registered MSMEs, Local POIs and Regional Price References for Hyper-Local Intelligence.
"""

from typing import List, Dict
from ..models.evidence import RegisteredMSMEItem, POIItem


SAMPLE_REGISTERED_MSMES: List[RegisteredMSMEItem] = [
    RegisteredMSMEItem(
        enterprise_id="msme_001",
        name="Shri Krishna Handlooms",
        category="handicraft_textiles",
        latitude=28.6150,
        longitude=77.2080,
        source="Udyam Registration Portal (2024-Q3 Data)",
        registration_year=2021
    ),
    RegisteredMSMEItem(
        enterprise_id="msme_002",
        name="Gramin Agro Flour & Spice Mills",
        category="food_processing_spices",
        latitude=28.6180,
        longitude=77.2150,
        source="Udyam Registration Portal (2024-Q3 Data)",
        registration_year=2022
    ),
    RegisteredMSMEItem(
        enterprise_id="msme_003",
        name="Kisan Kalyan Vermi Producer Co.",
        category="vermicompost_production",
        latitude=28.5900,
        longitude=77.1950,
        source="District Industries Center (DIC) Registry",
        registration_year=2023
    ),
    RegisteredMSMEItem(
        enterprise_id="msme_004",
        name="Kamdhenu Dairy Collection Unit",
        category="dairy_micro_farm",
        latitude=28.6320,
        longitude=77.1850,
        source="National Dairy Development Board Partner Registry",
        registration_year=2020
    ),
    RegisteredMSMEItem(
        enterprise_id="msme_005",
        name="Pratibha Boutique & Tailoring",
        category="garment_tailoring_unit",
        latitude=28.6100,
        longitude=77.2050,
        source="Udyam Registration Portal (2024-Q3 Data)",
        registration_year=2023
    ),
    RegisteredMSMEItem(
        enterprise_id="msme_006",
        name="Navjeevan Organic Bio Fertilizers",
        category="organic_farm_inputs",
        latitude=28.5850,
        longitude=77.2000,
        source="District Agriculture Office Record",
        registration_year=2022
    )
]

SAMPLE_POIS: List[POIItem] = [
    POIItem(
        poi_id="poi_001",
        name="Main Agricultural Produce Mandi",
        poi_type="APMC Mandi",
        latitude=28.6190,
        longitude=77.2140
    ),
    POIItem(
        poi_id="poi_002",
        name="Weekly Rural Haat & Crafts Fair",
        poi_type="Weekly Haat",
        latitude=28.6110,
        longitude=77.2090
    ),
    POIItem(
        poi_id="poi_003",
        name="District Cooperative Central Bank",
        poi_type="Cooperative Bank",
        latitude=28.6160,
        longitude=77.2070
    ),
    POIItem(
        poi_id="poi_004",
        name="Common Service Center (CSC) / Digital Hub",
        poi_type="CSC Center",
        latitude=28.6130,
        longitude=77.2040
    ),
    POIItem(
        poi_id="poi_005",
        name="Highway Logistics & Truck Terminal",
        poi_type="Transport Hub",
        latitude=28.6410,
        longitude=77.2510
    )
]

SAMPLE_REGIONAL_PRICES: Dict[str, Dict[str, str]] = {
    "handicraft_textiles": {
        "raw_jute_cotton": "₹120 - ₹180 / kg (Regional wholesale proxy)",
        "finished_handicraft_bag": "₹350 - ₹650 / piece (Local retail estimate)",
        "source": "State Handicrafts Development Corporation Price Index"
    },
    "dairy_micro_farm": {
        "raw_milk_procurement": "₹38 - ₹44 / liter (State Milk Union Benchmark)",
        "cow_feed": "₹28 / kg",
        "source": "State Cooperative Dairy Federation (e-NAM proxy)"
    },
    "vermicompost_production": {
        "vermicompost_bulk": "₹6 - ₹9 / kg (Farm gate price)",
        "earthworm_culture": "₹250 - ₹350 / kg",
        "source": "KVK (Krishi Vigyan Kendra) Price Advisory"
    },
    "food_processing_spices": {
        "raw_chilli_turmeric": "₹140 - ₹210 / kg (Mandi benchmark)",
        "packaged_powder": "₹320 - ₹450 / kg",
        "source": "APMC Mandi Realized Price Feed"
    }
}
