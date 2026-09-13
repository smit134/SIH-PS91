import os
from google import genai
from google.genai import types
from app.config import settings

def get_gemini_client():
    api_key = settings.GEMINI_API_KEY
    if not api_key:
        api_key = os.environ.get("GEMINI_API_KEY")
    return genai.Client(api_key=api_key)

def generate_chat_response(messages: list[dict], context_data: dict = None) -> str:
    """
    Generate a response using Gemini based on conversation history and current page context.
    messages format: [{"role": "user", "content": "..."}]
    """
    if not settings.GEMINI_API_KEY and not os.environ.get("GEMINI_API_KEY"):
        return "I am unable to answer right now because the GEMINI_API_KEY is not configured. Please add it to your .env file."
        
    client = get_gemini_client()
    
    # Construct system instruction
    system_instruction = (
        "You are ThinkForge Copilot, an AI assistant for rural entrepreneurs. "
        "CRITICAL INSTRUCTIONS: "
        "1. BE EXTREMELY CONCISE. Never write long paragraphs. "
        "2. Structure your output using short, scannable bullet points (use standard dashes '-') or numbered lists. "
        "3. Only provide the essential information required. Do not over-explain or provide unnecessary details. "
        "4. DO NOT use markdown like asterisks (**) or hashes (#), use plain text formatting only. "
        "5. The Omniscient Backend Context Data below provides the user's top opportunities, partners, and schemes regardless of what page they are on. Use this data to answer their questions!"
    )
    if context_data:
        system_instruction += f"\n\nOmniscient Backend Context Data:\n{context_data}"

    # Format history into a single input string for simplicity (since we aren't tracking previous_interaction_id)
    input_text = ""
    for msg in messages:
        role = "User" if msg["role"] == "user" else "Assistant"
        input_text += f"{role}: {msg['content']}\n"
        
    input_text += "Assistant: "

    try:
        interaction = client.interactions.create(
            model='gemini-3.6-flash',
            input=input_text,
            system_instruction=system_instruction,
            generation_config={"temperature": 0.2}
        )
        return interaction.output_text
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return "Sorry, I encountered an error while trying to generate a response. Please check the backend logs."

async def personalize_recommendations(profile, interactions, candidates) -> list:
    """
    Uses local Gemma model via Ollama to personalize and re-rank business opportunities.
    """
    import httpx
    import json
    
    # Format candidates
    candidate_desc = []
    for c in candidates:
        candidate_desc.append(f"ID: {c.business_id}, Title: {c.business_name}, Base Score: {c.overall_fit_score}")
        
    # Format interactions
    interaction_desc = []
    for i in interactions:
        interaction_desc.append(f"User {i.interaction_type.value} business ID: {i.business_id}")
        
    prompt = f"""
    You are an AI Business Advisor for rural entrepreneurs. 
    The user has a base profile and has interacted with some businesses.
    
    Interactions:
    {', '.join(interaction_desc) if interaction_desc else 'None yet.'}
    
    Candidates:
    {chr(10).join(candidate_desc)}
    
    TASK: Pick the top 5 best businesses from the Candidates list. Re-rank them based on the User's Interactions (e.g. if they DISLIKED something similar, rank it lower).
    For each, provide a brief 1-sentence 'ai_rationale' explaining why it fits them given their preferences.
    
    Output strictly in this JSON format:
    [
      {{"business_id": "...", "ai_rationale": "..."}}
    ]
    """
    
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post("http://host.docker.internal:11434/api/generate", json={
                "model": "gemma:2b",
                "prompt": prompt,
                "format": "json",
                "stream": False
            }, timeout=30.0)
            if resp.status_code == 200:
                data = resp.json()
                raw_response = data.get("response", "")
                
                # Strip backticks if present
                if raw_response.startswith("```json"):
                    raw_response = raw_response[7:]
                if raw_response.startswith("```"):
                    raw_response = raw_response[3:]
                if raw_response.endswith("```"):
                    raw_response = raw_response[:-3]
                    
                result = json.loads(raw_response.strip())
                
                if isinstance(result, dict) and "recommendations" in result:
                    result = result["recommendations"]
                
                # Merge back into candidate list and reorder
                ranked_candidates = []
                if isinstance(result, list):
                    for item in result:
                        if isinstance(item, dict):
                            b_id = item.get("business_id")
                            ai_rat = item.get("ai_rationale")
                        elif isinstance(item, str):
                            b_id = item
                            ai_rat = "Recommended by AI based on your preferences."
                        else:
                            continue
                            
                        # Find candidate
                        match = next((c for c in candidates if c.business_id == b_id), None)
                        if match:
                            match.ai_rationale = ai_rat
                            ranked_candidates.append(match)
                        
                # Add any missing ones at the end just in case the AI dropped them
                for c in candidates:
                    if c not in ranked_candidates:
                        ranked_candidates.append(c)
                        
                return ranked_candidates[:5]
    except Exception as e:
        print(f"Ollama AI Personalization failed: {e}")
        
    return candidates[:5]
