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
            model='gemini-3.7-flash',
            input=input_text,
            system_instruction=system_instruction,
            generation_config={"temperature": 0.2}
        )
        return interaction.output_text
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return "Sorry, I encountered an error while trying to generate a response. Please check the backend logs."
