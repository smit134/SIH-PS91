from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from services.llm_service import llm_service
import json

class RAGService:
    def __init__(self, db: Session):
        self.db = db

    def retrieve_evidence(self, query: str, top_k: int = 5) -> List[Any]:
        query_embedding = llm_service.generate_embedding(query)
        results = []
        
        # 1. Query Evidence table
        try:
            from models import Evidence
            evs = self.db.query(Evidence).order_by(
                Evidence.embedding.l2_distance(query_embedding)
            ).limit(top_k).all()
            results.extend(evs)
        except Exception as e:
            pass

        return results

    def retrieve_policy_chunks(self, query: str, top_k: int = 3) -> List[str]:
        """Queries vectorized government scheme guidelines (PMEGP, MUDRA) via pgvector."""
        query_embedding = llm_service.generate_embedding(query)
        chunks = []
        try:
            from app.models.document_chunk import SchemeDocumentChunk
            db_chunks = self.db.query(SchemeDocumentChunk).order_by(
                SchemeDocumentChunk.embedding.l2_distance(query_embedding)
            ).limit(top_k).all()
            for c in db_chunks:
                chunks.append(f"[{c.source_document} Page {c.page_number or 1}]\n{c.chunk_text}")
        except Exception:
            pass
        return chunks

    def generate_explanation(self, entrepreneur_context: str, recommendation: str, local_query: str) -> str:
        # Retrieve relevant local evidence and policy chunks
        evidences = self.retrieve_evidence(local_query)
        policy_chunks = self.retrieve_policy_chunks(local_query)
        
        context_parts = []
        for e in evidences:
            context_parts.append(f"[{getattr(e, 'evidence_type', 'Market Evidence')}] Source: {getattr(e, 'source', 'Local Registry')}\nContent: {getattr(e, 'content', '')}")
        for p in policy_chunks:
            context_parts.append(p)
            
        context_text = "\n\n".join(context_parts) if context_parts else "Benchmark MSME empirical dataset and regional demand indicators for Gujarat."
        
        try:
            from services.prompts import EXPLAINABILITY_SYSTEM_PROMPT
        except ImportError:
            EXPLAINABILITY_SYSTEM_PROMPT = (
                "You are an expert rural enterprise advisor. Provide a clear, factual, "
                "actionable explanation for rural micro-entrepreneurs."
            )
        
        prompt = (
            f"Entrepreneur Profile:\n{entrepreneur_context}\n\n"
            f"Recommended Business: {recommendation}\n\n"
            f"Local Evidence Context:\n{context_text}\n\n"
            "Explain why this business is suitable, key viability factors, and potential risks."
        )
        
        return llm_service.generate_completion(prompt, system_prompt=EXPLAINABILITY_SYSTEM_PROMPT)
