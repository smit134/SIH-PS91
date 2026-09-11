import sys
import os

sys.stdout.reconfigure(encoding='utf-8')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal
from services.rag_service import RAGService

def test_rag():
    print("Testing local RAG and LLM connection...")
    db = SessionLocal()
    rag = RAGService(db)

    entrepreneur_context = "Handicraft maker with 5 years experience. Rs. 30,000 budget."
    recommendation = "Handicraft retail business"
    local_query = "Handicrafts demand"

    try:
        print("Running RAG generation...")
        result = rag.generate_explanation(
            entrepreneur_context=entrepreneur_context,
            recommendation=recommendation,
            local_query=local_query
        )
        print("\n--- LLM Response ---")
        print(result)
        print("--------------------\n")
        print("Success! RAG pipeline and Ollama are fully functional.")
    except Exception as e:
        print(f"Error testing RAG: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    test_rag()
