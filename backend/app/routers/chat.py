from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel
from typing import List, Optional, Any
from app.services.llm_service import generate_chat_response

router = APIRouter()

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    context_data: Optional[Any] = None

class ChatResponse(BaseModel):
    response: str

@router.post("/", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest = Body(...)):
    """
    Endpoint for the AI Chatbot Assistant.
    """
    try:
        messages_dict = [{"role": msg.role, "content": msg.content} for msg in request.messages]
        
        # Build Backend RAG Context
        rag_context = ""
        try:
            import json
            from app.models.user import EntrepreneurProfile, LocationPoint
            from app.engines.opportunity_engine import OpportunityEngine
            from app.engines.partner_engine import PartnerMatchEngine
            from app.models.common import RiskLevel
            
            raw_data = request.context_data or {}
            profile_str = raw_data.get("user_profile_data", "{}")
            raw_profile = json.loads(profile_str) if profile_str else {}
            
            equity_str = str(raw_profile.get("ownEquity", "150000"))
            equity = int(''.join(filter(str.isdigit, equity_str)) or 150000)
            
            profile = EntrepreneurProfile(
                user_id="demo_user",
                name="Rural Entrepreneur",
                available_capital=equity,
                skills=[raw_profile.get("primarySkill", "Agri-Processing")],
                experience_years=2.0,
                resources=[raw_profile.get("landAccess", "Owned"), raw_profile.get("powerSupply", "3-Phase")],
                interests=[raw_profile.get("sectorInterest", "Post-Harvest")],
                location=LocationPoint(
                    latitude=20.7453,
                    longitude=78.6022,
                    village_or_town=raw_profile.get("block", "Deoli"),
                    district=raw_profile.get("district", "Wardha"),
                    state=raw_profile.get("state", "Maharashtra"),
                    service_radius_km=15.0
                ),
                risk_preference=RiskLevel.MEDIUM,
                has_transport_access=bool(raw_profile.get("transportVehicle", False)),
                has_market_connections=False,
                has_digital_tools=True
            )
            
            # Fetch backend data
            search_res = OpportunityEngine.reverse_business_search(profile)
            top_opps = [
                f"{opp.business_id} (Fit: {opp.overall_fit_score_percent}%): Cap: {opp.financial_feasibility.estimated_capital_required}, ROI: {opp.financial_feasibility.projected_roi_percent}%"
                for opp in search_res.ranked_opportunities[:3]
            ]
            
            partners = PartnerMatchEngine.find_matches(profile, max_radius_km=50.0)
            top_partners = [
                f"{p.name} ({p.type}) Synergy: {p.synergy_score}%"
                for p in partners[:3]
            ]
            
            import os
            schemes_path = os.path.join(os.path.dirname(__file__), "..", "data", "verified_datasets", "schemes.json")
            with open(schemes_path, "r") as f:
                schemes_data = json.load(f)
                schemes_info = [f"{s['title']}: {s.get('max_subsidy_percentage', 'N/A')}% Subsidy" for s in schemes_data[:3]]
                
            page_text = raw_data.get("page_text_content", "")
            page_title = raw_data.get("title", "")
            
            rag_context = (
                f"User Profile Info: {profile_str}\n"
                f"Current Page User is Viewing: {page_title}\n"
                f"Current Page Content: {page_text[:5000]}\n"
                f"Top 3 Opportunities from Backend Database: {top_opps}\n"
                f"Top 3 Partner Matches from Backend Database: {top_partners}\n"
                f"Top Government Schemes Available: {schemes_info}\n"
            )
        except Exception as e:
            rag_context = f"Failed to build RAG context: {e}"
        
        reply = generate_chat_response(messages_dict, rag_context)
        return ChatResponse(response=reply)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
