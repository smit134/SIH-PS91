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
        
    api_key = settings.GEMINI_API_KEY or os.environ.get("GEMINI_API_KEY")
    if api_key == "redacted":
        # Fallback Mock Mode when no real API key is provided
        last_message = messages[-1]["content"].lower()
        if "scheme" in last_message:
            return "Based on your profile, the top schemes available are:\n- PMEGP (Prime Minister's Employment Generation Programme)\n- PMFME (PM Formalisation of Micro food processing Enterprises)\n- AIF (Agriculture Infrastructure Fund)"
        elif "partner" in last_message or "fpo" in last_message:
            return "There are 3 FPOs and 2 Cold Storage units within a 20km radius that perfectly match your resource profile."
        elif "opportunity" in last_message or "business" in last_message:
            return "Your best opportunity is establishing an Agri-Briquette unit. It has an 83% fit with your current capital and skills."
        elif "dashboard" in last_message or "page" in last_message or "here" in last_message:
            return "You are currently viewing the ThinkForge dashboard. It shows your profile readiness, viable opportunities, and potential partners in your local area."
        else:
            return f"(Mock Mode) I am your ThinkForge Copilot! To get real AI answers, please configure a valid GEMINI_API_KEY in the backend .env file. You asked: '{messages[-1]['content']}'"

    client = get_gemini_client()
    
    # Construct system instruction
    system_instruction = (
        "You are ThinkForge Copilot, an AI assistant for rural entrepreneurs. "
        "CRITICAL INSTRUCTIONS: "
        "1. BE EXTREMELY CONCISE. Never write long paragraphs. "
        "2. Structure your output using short, scannable bullet points (use standard dashes '-') or numbered lists. "
        "3. Only provide the essential information required. Do not over-explain or provide unnecessary details. "
        "4. DO NOT use markdown like asterisks (**) or hashes (#), use plain text formatting only. "
        "5. The Omniscient Backend Context Data below provides the user's top opportunities, partners, and schemes. It also contains the CURRENT PAGE CONTENT. If the user asks a question about the website or what they are looking at, use the Current Page Content to answer them accurately!"
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
        response = client.models.generate_content(
            model='gemini-1.5-flash',
            contents=input_text,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.2,
            )
        )
        return response.text
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return f"Sorry, I encountered an error: {str(e)}"
