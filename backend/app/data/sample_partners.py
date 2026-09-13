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
            latitude=20.7500,
            longitude=78.6100,
            village_or_town="Wardha Market",
            district="Wardha District",
            state="Maharashtra",
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
            latitude=20.7600,
            longitude=78.6200,
            village_or_town="Deoli Block Center",
            district="Wardha District",
            state="Maharashtra",
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
            latitude=20.7300,
            longitude=78.5900,
            village_or_town="Hinganghat Village",
            district="Wardha District",
            state="Maharashtra",
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
            latitude=20.7700,
            longitude=78.5800,
            village_or_town="Milk Producers Hub",
            district="Wardha District",
            state="Maharashtra",
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
            latitude=20.7800,
            longitude=78.6500,
            village_or_town="Railway Junction Block",
            district="Wardha District",
            state="Maharashtra",
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
    ),

    PartnerProfile(
        partner_id="mock_partner_1",
        name="Rahul Reddy",
        phone="+91-9179921161",
        location=LocationPoint(
            latitude=19.2352,
            longitude=79.775,
            village_or_town="Village 74",
            district="Tamil Nadu District 2",
            state="Tamil Nadu",
            service_radius_km=37.2
        ),
        capabilities=['Distribution', 'Production'],
        skills=['Accounting', 'Management', 'Digital Literacy'],
        resources=['Water Pump'],
        investment_min=26000.0,
        investment_max=220000.0,
        experience_years=5.3,
        business_interests=['mock_business_43', 'mock_business_19', 'mock_business_5'],
        verification_state=VerificationState.BASIC
    ),
    PartnerProfile(
        partner_id="mock_partner_2",
        name="Kavita Reddy",
        phone="+91-9492689008",
        location=LocationPoint(
            latitude=20.4145,
            longitude=77.9136,
            village_or_town="Village 80",
            district="Tamil Nadu District 3",
            state="Tamil Nadu",
            service_radius_km=29.1
        ),
        capabilities=['Transport', 'Production', 'Technology', 'Management'],
        skills=['Farming', 'Carpentry', 'Driving'],
        resources=['Oven', 'Warehouse', 'Cold Storage'],
        investment_min=41000.0,
        investment_max=214000.0,
        experience_years=6.5,
        business_interests=['mock_business_15', 'mock_business_40', 'mock_business_33'],
        verification_state=VerificationState.BASIC
    ),
    PartnerProfile(
        partner_id="mock_partner_3",
        name="Rahul Reddy",
        phone="+91-9720236700",
        location=LocationPoint(
            latitude=20.556,
            longitude=79.1202,
            village_or_town="Village 38",
            district="Tamil Nadu District 4",
            state="Tamil Nadu",
            service_radius_km=18.2
        ),
        capabilities=['Transport', 'Capital', 'Raw Materials'],
        skills=['Carpentry', 'Marketing', 'Farming', 'Machine Operation'],
        resources=['Water Pump'],
        investment_min=21000.0,
        investment_max=89000.0,
        experience_years=1.9,
        business_interests=['mock_business_25', 'mock_business_23', 'mock_business_46'],
        verification_state=VerificationState.BASIC
    ),
    PartnerProfile(
        partner_id="mock_partner_4",
        name="Kavita Sharma",
        phone="+91-9619912546",
        location=LocationPoint(
            latitude=21.4275,
            longitude=77.9617,
            village_or_town="Village 53",
            district="Gujarat District 3",
            state="Gujarat",
            service_radius_km=38.2
        ),
        capabilities=['Marketing', 'Transport', 'Management', 'Distribution'],
        skills=['Accounting', 'Sales', 'Marketing', 'Packaging'],
        resources=['Shop', 'Land', 'Truck'],
        investment_min=37000.0,
        investment_max=134000.0,
        experience_years=1.2,
        business_interests=['mock_business_1', 'mock_business_14', 'mock_business_36'],
        verification_state=VerificationState.VERIFIED
    ),
    PartnerProfile(
        partner_id="mock_partner_5",
        name="Sneha Singh",
        phone="+91-9128239419",
        location=LocationPoint(
            latitude=21.7882,
            longitude=79.31,
            village_or_town="Village 66",
            district="Tamil Nadu District 5",
            state="Tamil Nadu",
            service_radius_km=16.6
        ),
        capabilities=['Technology', 'Distribution', 'Management', 'Capital'],
        skills=['Digital Literacy', 'Carpentry', 'Machine Operation'],
        resources=['Truck'],
        investment_min=25000.0,
        investment_max=98000.0,
        experience_years=4.4,
        business_interests=['mock_business_48', 'mock_business_5', 'mock_business_20'],
        verification_state=VerificationState.BASIC
    ),
    PartnerProfile(
        partner_id="mock_partner_6",
        name="Amit Patel",
        phone="+91-9729437821",
        location=LocationPoint(
            latitude=19.1666,
            longitude=76.4032,
            village_or_town="Village 22",
            district="Maharashtra District 4",
            state="Maharashtra",
            service_radius_km=25.2
        ),
        capabilities=['Transport', 'Management'],
        skills=['Sales', 'Digital Literacy', 'Machine Operation', 'Management'],
        resources=['Shop'],
        investment_min=37000.0,
        investment_max=233000.0,
        experience_years=8.0,
        business_interests=['mock_business_12', 'mock_business_40', 'mock_business_14'],
        verification_state=VerificationState.VERIFIED
    ),
    PartnerProfile(
        partner_id="mock_partner_7",
        name="Anjali Das",
        phone="+91-9870291757",
        location=LocationPoint(
            latitude=19.2356,
            longitude=78.6302,
            village_or_town="Village 3",
            district="Maharashtra District 3",
            state="Maharashtra",
            service_radius_km=17.9
        ),
        capabilities=['Raw Materials', 'Distribution'],
        skills=['Farming', 'Machine Operation', 'Digital Literacy', 'Carpentry'],
        resources=['Warehouse', 'Oven', 'Cold Storage'],
        investment_min=28000.0,
        investment_max=117000.0,
        experience_years=6.5,
        business_interests=['mock_business_13', 'mock_business_12', 'mock_business_31'],
        verification_state=VerificationState.VERIFIED
    ),
    PartnerProfile(
        partner_id="mock_partner_8",
        name="Priya Sharma",
        phone="+91-9311499122",
        location=LocationPoint(
            latitude=21.8866,
            longitude=79.351,
            village_or_town="Village 4",
            district="Maharashtra District 5",
            state="Maharashtra",
            service_radius_km=15.7
        ),
        capabilities=['Transport', 'Production'],
        skills=['Sales', 'Digital Literacy', 'Management'],
        resources=['Land'],
        investment_min=18000.0,
        investment_max=147000.0,
        experience_years=9.5,
        business_interests=['mock_business_12', 'mock_business_37', 'mock_business_50'],
        verification_state=VerificationState.VERIFIED
    ),
    PartnerProfile(
        partner_id="mock_partner_9",
        name="Rahul Yadav",
        phone="+91-9921106443",
        location=LocationPoint(
            latitude=19.4215,
            longitude=79.3412,
            village_or_town="Village 99",
            district="Rajasthan District 5",
            state="Rajasthan",
            service_radius_km=21.3
        ),
        capabilities=['Technology', 'Marketing'],
        skills=['Management', 'Sales'],
        resources=['Tractor', 'Water Pump'],
        investment_min=32000.0,
        investment_max=205000.0,
        experience_years=12.0,
        business_interests=['mock_business_18', 'mock_business_7', 'mock_business_44'],
        verification_state=VerificationState.VERIFIED
    ),
    PartnerProfile(
        partner_id="mock_partner_10",
        name="Meena Yadav",
        phone="+91-9214530395",
        location=LocationPoint(
            latitude=21.7353,
            longitude=78.0095,
            village_or_town="Village 49",
            district="Rajasthan District 2",
            state="Rajasthan",
            service_radius_km=12.6
        ),
        capabilities=['Technology', 'Capital'],
        skills=['Marketing', 'Packaging'],
        resources=['Truck', 'Shop'],
        investment_min=42000.0,
        investment_max=242000.0,
        experience_years=2.6,
        business_interests=['mock_business_14', 'mock_business_17', 'mock_business_2'],
        verification_state=VerificationState.VERIFIED
    ),
    PartnerProfile(
        partner_id="mock_partner_11",
        name="Meena Rao",
        phone="+91-9754623780",
        location=LocationPoint(
            latitude=18.029,
            longitude=76.1236,
            village_or_town="Village 22",
            district="UP District 4",
            state="UP",
            service_radius_km=34.2
        ),
        capabilities=['Transport', 'Technology'],
        skills=['Marketing', 'Digital Literacy', 'Driving'],
        resources=['Computer'],
        investment_min=42000.0,
        investment_max=236000.0,
        experience_years=10.8,
        business_interests=['mock_business_2', 'mock_business_19', 'mock_business_29'],
        verification_state=VerificationState.BASIC
    ),
    PartnerProfile(
        partner_id="mock_partner_12",
        name="Rohan Das",
        phone="+91-9905389467",
        location=LocationPoint(
            latitude=18.107,
            longitude=79.0252,
            village_or_town="Village 59",
            district="Gujarat District 4",
            state="Gujarat",
            service_radius_km=10.4
        ),
        capabilities=['Transport', 'Capital', 'Logistics'],
        skills=['Sewing', 'Management', 'Driving'],
        resources=['Water Pump', 'Sewing Machine', 'Warehouse'],
        investment_min=36000.0,
        investment_max=191000.0,
        experience_years=14.7,
        business_interests=['mock_business_13', 'mock_business_43', 'mock_business_43'],
        verification_state=VerificationState.BASIC
    ),
    PartnerProfile(
        partner_id="mock_partner_13",
        name="Amit Sharma",
        phone="+91-9575927350",
        location=LocationPoint(
            latitude=20.9264,
            longitude=78.7142,
            village_or_town="Village 66",
            district="Tamil Nadu District 3",
            state="Tamil Nadu",
            service_radius_km=21.9
        ),
        capabilities=['Distribution', 'Production', 'Marketing', 'Management'],
        skills=['Sewing', 'Marketing', 'Machine Operation', 'Management'],
        resources=['Land', 'Tractor', 'Shop'],
        investment_min=33000.0,
        investment_max=200000.0,
        experience_years=8.8,
        business_interests=['mock_business_33', 'mock_business_1', 'mock_business_50'],
        verification_state=VerificationState.BASIC
    ),
    PartnerProfile(
        partner_id="mock_partner_14",
        name="Vikram Yadav",
        phone="+91-9416168937",
        location=LocationPoint(
            latitude=20.1461,
            longitude=78.8057,
            village_or_town="Village 66",
            district="Tamil Nadu District 1",
            state="Tamil Nadu",
            service_radius_km=38.9
        ),
        capabilities=['Raw Materials', 'Management', 'Logistics', 'Transport'],
        skills=['Management', 'Driving', 'Sales'],
        resources=['Truck'],
        investment_min=28000.0,
        investment_max=172000.0,
        experience_years=7.9,
        business_interests=['mock_business_48', 'mock_business_49', 'mock_business_23'],
        verification_state=VerificationState.VERIFIED
    ),
    PartnerProfile(
        partner_id="mock_partner_15",
        name="Suresh Singh",
        phone="+91-9739395426",
        location=LocationPoint(
            latitude=19.1141,
            longitude=76.4532,
            village_or_town="Village 9",
            district="Maharashtra District 4",
            state="Maharashtra",
            service_radius_km=30.1
        ),
        capabilities=['Logistics', 'Marketing', 'Distribution'],
        skills=['Sales', 'Accounting'],
        resources=['Warehouse', 'Shop'],
        investment_min=22000.0,
        investment_max=87000.0,
        experience_years=9.2,
        business_interests=['mock_business_23', 'mock_business_16', 'mock_business_50'],
        verification_state=VerificationState.BASIC
    ),
    PartnerProfile(
        partner_id="mock_partner_16",
        name="Suresh Reddy",
        phone="+91-9537814717",
        location=LocationPoint(
            latitude=21.7899,
            longitude=76.3738,
            village_or_town="Village 90",
            district="MP District 4",
            state="MP",
            service_radius_km=15.2
        ),
        capabilities=['Production', 'Management', 'Distribution', 'Technology'],
        skills=['Farming', 'Machine Operation', 'Carpentry'],
        resources=['Truck', 'Warehouse', 'Water Pump'],
        investment_min=16000.0,
        investment_max=119000.0,
        experience_years=2.0,
        business_interests=['mock_business_30', 'mock_business_1', 'mock_business_46'],
        verification_state=VerificationState.BASIC
    ),
    PartnerProfile(
        partner_id="mock_partner_17",
        name="Rahul Gupta",
        phone="+91-9105837272",
        location=LocationPoint(
            latitude=18.0012,
            longitude=77.2184,
            village_or_town="Village 89",
            district="Maharashtra District 4",
            state="Maharashtra",
            service_radius_km=22.3
        ),
        capabilities=['Distribution', 'Management', 'Capital'],
        skills=['Carpentry', 'Sewing'],
        resources=['Oven'],
        investment_min=15000.0,
        investment_max=169000.0,
        experience_years=11.3,
        business_interests=['mock_business_8', 'mock_business_8', 'mock_business_13'],
        verification_state=VerificationState.BASIC
    ),
    PartnerProfile(
        partner_id="mock_partner_18",
        name="Sneha Rao",
        phone="+91-9229321781",
        location=LocationPoint(
            latitude=20.3792,
            longitude=76.7534,
            village_or_town="Village 59",
            district="Rajasthan District 1",
            state="Rajasthan",
            service_radius_km=23.5
        ),
        capabilities=['Logistics', 'Capital'],
        skills=['Carpentry', 'Sewing', 'Accounting'],
        resources=['Shop', 'Warehouse'],
        investment_min=13000.0,
        investment_max=195000.0,
        experience_years=11.0,
        business_interests=['mock_business_37', 'mock_business_37', 'mock_business_11'],
        verification_state=VerificationState.BASIC
    ),
    PartnerProfile(
        partner_id="mock_partner_19",
        name="Vikram Rao",
        phone="+91-9733680871",
        location=LocationPoint(
            latitude=19.4261,
            longitude=79.5508,
            village_or_town="Village 34",
            district="Tamil Nadu District 5",
            state="Tamil Nadu",
            service_radius_km=39.8
        ),
        capabilities=['Production', 'Distribution', 'Logistics', 'Marketing'],
        skills=['Packaging', 'Carpentry', 'Sewing'],
        resources=['Warehouse', 'Cold Storage', 'Sewing Machine'],
        investment_min=46000.0,
        investment_max=104000.0,
        experience_years=2.2,
        business_interests=['mock_business_31', 'mock_business_41', 'mock_business_29'],
        verification_state=VerificationState.BASIC
    ),
    PartnerProfile(
        partner_id="mock_partner_20",
        name="Kavita Gupta",
        phone="+91-9729897200",
        location=LocationPoint(
            latitude=18.9411,
            longitude=76.3348,
            village_or_town="Village 53",
            district="Maharashtra District 3",
            state="Maharashtra",
            service_radius_km=15.3
        ),
        capabilities=['Logistics', 'Transport', 'Management'],
        skills=['Accounting', 'Management', 'Farming'],
        resources=['Cold Storage', 'Water Pump', 'Shop'],
        investment_min=17000.0,
        investment_max=107000.0,
        experience_years=6.9,
        business_interests=['mock_business_12', 'mock_business_8', 'mock_business_10'],
        verification_state=VerificationState.VERIFIED
    ),
    PartnerProfile(
        partner_id="mock_partner_21",
        name="Vikram Das",
        phone="+91-9681344298",
        location=LocationPoint(
            latitude=20.7408,
            longitude=76.9181,
            village_or_town="Village 1",
            district="Gujarat District 2",
            state="Gujarat",
            service_radius_km=40.8
        ),
        capabilities=['Management', 'Logistics', 'Transport'],
        skills=['Carpentry', 'Digital Literacy'],
        resources=['Sewing Machine', 'Warehouse', 'Truck'],
        investment_min=43000.0,
        investment_max=209000.0,
        experience_years=12.5,
        business_interests=['mock_business_35', 'mock_business_49', 'mock_business_35'],
        verification_state=VerificationState.VERIFIED
    ),
    PartnerProfile(
        partner_id="mock_partner_22",
        name="Rahul Das",
        phone="+91-9650416520",
        location=LocationPoint(
            latitude=18.7728,
            longitude=77.7363,
            village_or_town="Village 50",
            district="UP District 4",
            state="UP",
            service_radius_km=13.6
        ),
        capabilities=['Production', 'Transport', 'Technology'],
        skills=['Accounting', 'Management', 'Carpentry', 'Packaging'],
        resources=['Land', 'Cold Storage'],
        investment_min=34000.0,
        investment_max=222000.0,
        experience_years=11.9,
        business_interests=['mock_business_38', 'mock_business_4', 'mock_business_24'],
        verification_state=VerificationState.BASIC
    ),
    PartnerProfile(
        partner_id="mock_partner_23",
        name="Sneha Singh",
        phone="+91-9497229472",
        location=LocationPoint(
            latitude=19.0639,
            longitude=76.7196,
            village_or_town="Village 2",
            district="Karnataka District 4",
            state="Karnataka",
            service_radius_km=40.0
        ),
        capabilities=['Production', 'Raw Materials'],
        skills=['Carpentry', 'Marketing'],
        resources=['Land', 'Computer'],
        investment_min=40000.0,
        investment_max=104000.0,
        experience_years=5.6,
        business_interests=['mock_business_12', 'mock_business_24', 'mock_business_34'],
        verification_state=VerificationState.BASIC
    ),
    PartnerProfile(
        partner_id="mock_partner_24",
        name="Meena Patel",
        phone="+91-9403548981",
        location=LocationPoint(
            latitude=20.2997,
            longitude=76.2768,
            village_or_town="Village 91",
            district="UP District 2",
            state="UP",
            service_radius_km=45.5
        ),
        capabilities=['Raw Materials', 'Transport'],
        skills=['Digital Literacy', 'Farming', 'Driving', 'Marketing'],
        resources=['Cold Storage', 'Sewing Machine', 'Land'],
        investment_min=38000.0,
        investment_max=235000.0,
        experience_years=5.1,
        business_interests=['mock_business_11', 'mock_business_50', 'mock_business_35'],
        verification_state=VerificationState.BASIC
    ),
    PartnerProfile(
        partner_id="mock_partner_25",
        name="Sneha Gupta",
        phone="+91-9282667321",
        location=LocationPoint(
            latitude=21.1603,
            longitude=79.2532,
            village_or_town="Village 62",
            district="Rajasthan District 2",
            state="Rajasthan",
            service_radius_km=33.1
        ),
        capabilities=['Management', 'Distribution', 'Transport', 'Marketing'],
        skills=['Farming', 'Sewing'],
        resources=['Tractor'],
        investment_min=49000.0,
        investment_max=136000.0,
        experience_years=2.3,
        business_interests=['mock_business_16', 'mock_business_14', 'mock_business_8'],
        verification_state=VerificationState.BASIC
    ),
    PartnerProfile(
        partner_id="mock_partner_26",
        name="Meena Reddy",
        phone="+91-9292346012",
        location=LocationPoint(
            latitude=18.9186,
            longitude=78.6273,
            village_or_town="Village 84",
            district="MP District 5",
            state="MP",
            service_radius_km=45.2
        ),
        capabilities=['Distribution', 'Production'],
        skills=['Carpentry', 'Sales', 'Machine Operation'],
        resources=['Oven'],
        investment_min=27000.0,
        investment_max=169000.0,
        experience_years=11.7,
        business_interests=['mock_business_39', 'mock_business_23', 'mock_business_32'],
        verification_state=VerificationState.VERIFIED
    ),
    PartnerProfile(
        partner_id="mock_partner_27",
        name="Rahul Sharma",
        phone="+91-9324084960",
        location=LocationPoint(
            latitude=19.3722,
            longitude=76.1939,
            village_or_town="Village 69",
            district="Karnataka District 1",
            state="Karnataka",
            service_radius_km=24.0
        ),
        capabilities=['Logistics', 'Technology', 'Capital'],
        skills=['Carpentry', 'Driving', 'Digital Literacy'],
        resources=['Sewing Machine'],
        investment_min=47000.0,
        investment_max=185000.0,
        experience_years=6.5,
        business_interests=['mock_business_33', 'mock_business_5', 'mock_business_14'],
        verification_state=VerificationState.BASIC
    ),
    PartnerProfile(
        partner_id="mock_partner_28",
        name="Kavita Rao",
        phone="+91-9609558938",
        location=LocationPoint(
            latitude=18.3722,
            longitude=77.5435,
            village_or_town="Village 78",
            district="MP District 1",
            state="MP",
            service_radius_km=42.0
        ),
        capabilities=['Logistics', 'Marketing'],
        skills=['Sales', 'Carpentry', 'Accounting'],
        resources=['Computer'],
        investment_min=14000.0,
        investment_max=168000.0,
        experience_years=8.8,
        business_interests=['mock_business_44', 'mock_business_19', 'mock_business_42'],
        verification_state=VerificationState.VERIFIED
    ),
    PartnerProfile(
        partner_id="mock_partner_29",
        name="Rohan Patel",
        phone="+91-9875750703",
        location=LocationPoint(
            latitude=19.311,
            longitude=78.3558,
            village_or_town="Village 27",
            district="Karnataka District 3",
            state="Karnataka",
            service_radius_km=15.7
        ),
        capabilities=['Technology', 'Capital'],
        skills=['Marketing', 'Digital Literacy', 'Driving', 'Farming'],
        resources=['Truck', 'Computer'],
        investment_min=36000.0,
        investment_max=123000.0,
        experience_years=8.4,
        business_interests=['mock_business_35', 'mock_business_37', 'mock_business_28'],
        verification_state=VerificationState.BASIC
    ),
    PartnerProfile(
        partner_id="mock_partner_30",
        name="Priya Jain",
        phone="+91-9414675537",
        location=LocationPoint(
            latitude=21.5999,
            longitude=76.6307,
            village_or_town="Village 93",
            district="Gujarat District 3",
            state="Gujarat",
            service_radius_km=19.6
        ),
        capabilities=['Distribution', 'Capital', 'Marketing'],
        skills=['Driving', 'Machine Operation', 'Sewing', 'Digital Literacy'],
        resources=['Computer', 'Truck', 'Cold Storage'],
        investment_min=12000.0,
        investment_max=94000.0,
        experience_years=8.3,
        business_interests=['mock_business_4', 'mock_business_43', 'mock_business_18'],
        verification_state=VerificationState.BASIC
    ),
    PartnerProfile(
        partner_id="mock_partner_31",
        name="Suresh Patel",
        phone="+91-9523972696",
        location=LocationPoint(
            latitude=19.6515,
            longitude=78.5309,
            village_or_town="Village 77",
            district="Gujarat District 3",
            state="Gujarat",
            service_radius_km=23.7
        ),
        capabilities=['Logistics', 'Management'],
        skills=['Carpentry', 'Sales'],
        resources=['Land'],
        investment_min=41000.0,
        investment_max=169000.0,
        experience_years=10.4,
        business_interests=['mock_business_38', 'mock_business_6', 'mock_business_41'],
        verification_state=VerificationState.BASIC
    ),
    PartnerProfile(
        partner_id="mock_partner_32",
        name="Vikram Patel",
        phone="+91-9890899628",
        location=LocationPoint(
            latitude=20.287,
            longitude=77.9082,
            village_or_town="Village 17",
            district="UP District 1",
            state="UP",
            service_radius_km=38.8
        ),
        capabilities=['Transport', 'Raw Materials', 'Technology', 'Marketing'],
        skills=['Farming', 'Packaging', 'Carpentry'],
        resources=['Sewing Machine', 'Truck'],
        investment_min=29000.0,
        investment_max=112000.0,
        experience_years=4.3,
        business_interests=['mock_business_30', 'mock_business_13', 'mock_business_25'],
        verification_state=VerificationState.BASIC
    ),
    PartnerProfile(
        partner_id="mock_partner_33",
        name="Anjali Jain",
        phone="+91-9186672065",
        location=LocationPoint(
            latitude=18.0873,
            longitude=77.0902,
            village_or_town="Village 36",
            district="Karnataka District 2",
            state="Karnataka",
            service_radius_km=33.3
        ),
        capabilities=['Capital', 'Transport', 'Raw Materials'],
        skills=['Farming', 'Accounting', 'Driving', 'Sewing'],
        resources=['Sewing Machine', 'Computer', 'Warehouse'],
        investment_min=14000.0,
        investment_max=106000.0,
        experience_years=9.0,
        business_interests=['mock_business_37', 'mock_business_50', 'mock_business_6'],
        verification_state=VerificationState.BASIC
    ),
    PartnerProfile(
        partner_id="mock_partner_34",
        name="Anjali Kumar",
        phone="+91-9607894109",
        location=LocationPoint(
            latitude=19.2941,
            longitude=76.4895,
            village_or_town="Village 77",
            district="Karnataka District 3",
            state="Karnataka",
            service_radius_km=46.9
        ),
        capabilities=['Capital', 'Distribution', 'Logistics', 'Management'],
        skills=['Sewing', 'Machine Operation', 'Sales'],
        resources=['Land', 'Oven'],
        investment_min=24000.0,
        investment_max=196000.0,
        experience_years=13.2,
        business_interests=['mock_business_13', 'mock_business_20', 'mock_business_39'],
        verification_state=VerificationState.BASIC
    ),
    PartnerProfile(
        partner_id="mock_partner_35",
        name="Suresh Gupta",
        phone="+91-9542789705",
        location=LocationPoint(
            latitude=21.5746,
            longitude=76.3969,
            village_or_town="Village 41",
            district="MP District 3",
            state="MP",
            service_radius_km=34.9
        ),
        capabilities=['Transport', 'Production'],
        skills=['Machine Operation', 'Accounting', 'Digital Literacy'],
        resources=['Cold Storage', 'Truck', 'Warehouse'],
        investment_min=13000.0,
        investment_max=154000.0,
        experience_years=12.5,
        business_interests=['mock_business_45', 'mock_business_32', 'mock_business_44'],
        verification_state=VerificationState.BASIC
    ),
    PartnerProfile(
        partner_id="mock_partner_36",
        name="Meena Singh",
        phone="+91-9374548153",
        location=LocationPoint(
            latitude=21.3023,
            longitude=78.0645,
            village_or_town="Village 51",
            district="MP District 1",
            state="MP",
            service_radius_km=12.7
        ),
        capabilities=['Production', 'Transport'],
        skills=['Driving', 'Packaging'],
        resources=['Cold Storage', 'Truck'],
        investment_min=36000.0,
        investment_max=175000.0,
        experience_years=14.1,
        business_interests=['mock_business_11', 'mock_business_31', 'mock_business_49'],
        verification_state=VerificationState.VERIFIED
    ),
    PartnerProfile(
        partner_id="mock_partner_37",
        name="Kavita Sharma",
        phone="+91-9640121127",
        location=LocationPoint(
            latitude=18.2091,
            longitude=76.7451,
            village_or_town="Village 39",
            district="MP District 5",
            state="MP",
            service_radius_km=13.0
        ),
        capabilities=['Distribution', 'Management', 'Marketing'],
        skills=['Driving', 'Accounting', 'Sewing'],
        resources=['Tractor'],
        investment_min=11000.0,
        investment_max=133000.0,
        experience_years=12.5,
        business_interests=['mock_business_29', 'mock_business_39', 'mock_business_42'],
        verification_state=VerificationState.BASIC
    ),
    PartnerProfile(
        partner_id="mock_partner_38",
        name="Kavita Reddy",
        phone="+91-9995146400",
        location=LocationPoint(
            latitude=19.624,
            longitude=77.7426,
            village_or_town="Village 76",
            district="MP District 2",
            state="MP",
            service_radius_km=16.7
        ),
        capabilities=['Transport', 'Raw Materials', 'Marketing'],
        skills=['Carpentry', 'Management', 'Packaging', 'Sales'],
        resources=['Oven', 'Sewing Machine'],
        investment_min=16000.0,
        investment_max=212000.0,
        experience_years=8.2,
        business_interests=['mock_business_44', 'mock_business_7', 'mock_business_17'],
        verification_state=VerificationState.BASIC
    ),
    PartnerProfile(
        partner_id="mock_partner_39",
        name="Suresh Rao",
        phone="+91-9938079442",
        location=LocationPoint(
            latitude=18.7519,
            longitude=76.762,
            village_or_town="Village 75",
            district="UP District 1",
            state="UP",
            service_radius_km=47.8
        ),
        capabilities=['Logistics', 'Transport', 'Marketing'],
        skills=['Farming', 'Management'],
        resources=['Cold Storage'],
        investment_min=16000.0,
        investment_max=153000.0,
        experience_years=14.5,
        business_interests=['mock_business_3', 'mock_business_23', 'mock_business_40'],
        verification_state=VerificationState.VERIFIED
    ),
    PartnerProfile(
        partner_id="mock_partner_40",
        name="Rohan Das",
        phone="+91-9465611919",
        location=LocationPoint(
            latitude=21.0971,
            longitude=76.7147,
            village_or_town="Village 27",
            district="Rajasthan District 3",
            state="Rajasthan",
            service_radius_km=34.4
        ),
        capabilities=['Raw Materials', 'Transport', 'Production', 'Capital'],
        skills=['Machine Operation', 'Marketing', 'Farming'],
        resources=['Sewing Machine'],
        investment_min=18000.0,
        investment_max=68000.0,
        experience_years=4.2,
        business_interests=['mock_business_1', 'mock_business_25', 'mock_business_33'],
        verification_state=VerificationState.BASIC
    ),
    PartnerProfile(
        partner_id="mock_partner_41",
        name="Suresh Gupta",
        phone="+91-9591010930",
        location=LocationPoint(
            latitude=21.7635,
            longitude=79.6433,
            village_or_town="Village 99",
            district="Rajasthan District 2",
            state="Rajasthan",
            service_radius_km=12.0
        ),
        capabilities=['Capital', 'Management', 'Transport'],
        skills=['Sales', 'Driving', 'Carpentry'],
        resources=['Tractor', 'Computer'],
        investment_min=37000.0,
        investment_max=173000.0,
        experience_years=3.2,
        business_interests=['mock_business_8', 'mock_business_48', 'mock_business_28'],
        verification_state=VerificationState.VERIFIED
    ),
    PartnerProfile(
        partner_id="mock_partner_42",
        name="Kavita Rao",
        phone="+91-9623612829",
        location=LocationPoint(
            latitude=19.0126,
            longitude=76.6993,
            village_or_town="Village 32",
            district="Rajasthan District 5",
            state="Rajasthan",
            service_radius_km=32.9
        ),
        capabilities=['Transport', 'Management'],
        skills=['Machine Operation', 'Marketing'],
        resources=['Truck', 'Tractor', 'Cold Storage'],
        investment_min=16000.0,
        investment_max=174000.0,
        experience_years=2.4,
        business_interests=['mock_business_11', 'mock_business_35', 'mock_business_15'],
        verification_state=VerificationState.BASIC
    ),
    PartnerProfile(
        partner_id="mock_partner_43",
        name="Sneha Kumar",
        phone="+91-9185727997",
        location=LocationPoint(
            latitude=21.3523,
            longitude=77.4713,
            village_or_town="Village 8",
            district="Maharashtra District 4",
            state="Maharashtra",
            service_radius_km=39.2
        ),
        capabilities=['Transport', 'Technology', 'Production'],
        skills=['Sales', 'Sewing', 'Machine Operation'],
        resources=['Land', 'Water Pump', 'Oven'],
        investment_min=44000.0,
        investment_max=131000.0,
        experience_years=11.7,
        business_interests=['mock_business_33', 'mock_business_2', 'mock_business_8'],
        verification_state=VerificationState.BASIC
    ),
    PartnerProfile(
        partner_id="mock_partner_44",
        name="Anjali Rao",
        phone="+91-9539403860",
        location=LocationPoint(
            latitude=20.9389,
            longitude=79.8669,
            village_or_town="Village 70",
            district="UP District 4",
            state="UP",
            service_radius_km=44.7
        ),
        capabilities=['Technology', 'Capital'],
        skills=['Sewing', 'Sales'],
        resources=['Truck', 'Tractor', 'Land'],
        investment_min=48000.0,
        investment_max=243000.0,
        experience_years=12.5,
        business_interests=['mock_business_45', 'mock_business_13', 'mock_business_46'],
        verification_state=VerificationState.BASIC
    ),
    PartnerProfile(
        partner_id="mock_partner_45",
        name="Kavita Gupta",
        phone="+91-9343458810",
        location=LocationPoint(
            latitude=19.8479,
            longitude=78.0133,
            village_or_town="Village 56",
            district="Tamil Nadu District 2",
            state="Tamil Nadu",
            service_radius_km=40.2
        ),
        capabilities=['Raw Materials', 'Transport'],
        skills=['Management', 'Sales', 'Accounting', 'Farming'],
        resources=['Computer', 'Water Pump', 'Cold Storage'],
        investment_min=14000.0,
        investment_max=202000.0,
        experience_years=13.3,
        business_interests=['mock_business_17', 'mock_business_11', 'mock_business_43'],
        verification_state=VerificationState.VERIFIED
    ),
    PartnerProfile(
        partner_id="mock_partner_46",
        name="Suresh Yadav",
        phone="+91-9337535791",
        location=LocationPoint(
            latitude=20.7847,
            longitude=77.5556,
            village_or_town="Village 88",
            district="Karnataka District 2",
            state="Karnataka",
            service_radius_km=32.7
        ),
        capabilities=['Raw Materials', 'Marketing'],
        skills=['Accounting', 'Marketing', 'Carpentry'],
        resources=['Land', 'Truck'],
        investment_min=18000.0,
        investment_max=75000.0,
        experience_years=11.5,
        business_interests=['mock_business_37', 'mock_business_42', 'mock_business_3'],
        verification_state=VerificationState.VERIFIED
    ),
    PartnerProfile(
        partner_id="mock_partner_47",
        name="Anjali Das",
        phone="+91-9563369935",
        location=LocationPoint(
            latitude=18.1346,
            longitude=76.5592,
            village_or_town="Village 44",
            district="Maharashtra District 2",
            state="Maharashtra",
            service_radius_km=14.0
        ),
        capabilities=['Technology', 'Distribution'],
        skills=['Sewing', 'Sales'],
        resources=['Computer', 'Water Pump'],
        investment_min=10000.0,
        investment_max=106000.0,
        experience_years=12.9,
        business_interests=['mock_business_44', 'mock_business_48', 'mock_business_25'],
        verification_state=VerificationState.BASIC
    ),
    PartnerProfile(
        partner_id="mock_partner_48",
        name="Sneha Reddy",
        phone="+91-9196015983",
        location=LocationPoint(
            latitude=18.8493,
            longitude=78.1101,
            village_or_town="Village 85",
            district="MP District 5",
            state="MP",
            service_radius_km=24.6
        ),
        capabilities=['Transport', 'Distribution', 'Raw Materials', 'Management'],
        skills=['Machine Operation', 'Accounting'],
        resources=['Sewing Machine', 'Oven', 'Warehouse'],
        investment_min=23000.0,
        investment_max=173000.0,
        experience_years=3.0,
        business_interests=['mock_business_48', 'mock_business_1', 'mock_business_25'],
        verification_state=VerificationState.BASIC
    ),
    PartnerProfile(
        partner_id="mock_partner_49",
        name="Rohan Yadav",
        phone="+91-9199188859",
        location=LocationPoint(
            latitude=19.8262,
            longitude=77.6602,
            village_or_town="Village 17",
            district="Rajasthan District 2",
            state="Rajasthan",
            service_radius_km=35.9
        ),
        capabilities=['Transport', 'Distribution', 'Management', 'Raw Materials'],
        skills=['Marketing', 'Packaging', 'Digital Literacy'],
        resources=['Cold Storage'],
        investment_min=47000.0,
        investment_max=183000.0,
        experience_years=6.5,
        business_interests=['mock_business_1', 'mock_business_11', 'mock_business_8'],
        verification_state=VerificationState.VERIFIED
    ),
    PartnerProfile(
        partner_id="mock_partner_50",
        name="Suresh Gupta",
        phone="+91-9164849849",
        location=LocationPoint(
            latitude=20.4839,
            longitude=78.8818,
            village_or_town="Village 18",
            district="Gujarat District 1",
            state="Gujarat",
            service_radius_km=12.8
        ),
        capabilities=['Management', 'Technology', 'Transport'],
        skills=['Sales', 'Management'],
        resources=['Shop', 'Tractor'],
        investment_min=49000.0,
        investment_max=107000.0,
        experience_years=4.0,
        business_interests=['mock_business_18', 'mock_business_5', 'mock_business_45'],
        verification_state=VerificationState.BASIC
    ),
]
