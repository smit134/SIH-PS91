from typing import List, Dict, Any
from sqlalchemy.orm import Session
from services.llm_service import llm_service
from models import Evidence
import json

class RAGService:
    def __init__(self, db: Session):
        self.db = db

    def retrieve_evidence(self, query: str, top_k: int = 5) -> List[Evidence]:
        query_embedding = llm_service.generate_embedding(query)
        
        # Use pgvector's L2 distance operator `<->` to find nearest neighbors
        # Ensure the vector is correctly formatted for SQLAlchemy
        results = self.db.query(Evidence).order_by(
            Evidence.embedding.l2_distance(query_embedding)
        ).limit(top_k).all()
        
        return results

    def generate_explanation(self, entrepreneur_context: str, recommendation: str, local_query: str) -> str:
        # Retrieve relevant local evidence
        evidences = self.retrieve_evidence(local_query)
        
        context_text = "\n\n".join([f"[{e.evidence_type}] Source: {e.source}\nContent: {e.content}" for e in evidences])
        
        from services.prompts import EXPLAINABILITY_SYSTEM_PROMPT
        
        prompt = (
            f"Entrepreneur Profile:\n{entrepreneur_context}\n\n"
            f"Recommended Business: {recommendation}\n\n"
            f"Local Evidence Context:\n{context_text}\n\n"
            "Explain why this business is suitable or what the risks are."
        )
        
        return llm_service.generate_completion(prompt, system_prompt=EXPLAINABILITY_SYSTEM_PROMPT)
