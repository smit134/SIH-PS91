
"""Document Chunk Model for RAG Vector Search (pgvector).

Stores chunked text passages from official government scheme PDFs
(PMEGP, MUDRA guidelines) with 768-dim embeddings for semantic retrieval.
"""

from typing import Any, Dict, Optional
from pgvector.sqlalchemy import Vector
from sqlalchemy import Column, Index, Integer, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class SchemeDocumentChunk(Base):
    """Vectorized document chunk for RAG-based scheme explanation."""

    __tablename__ = "scheme_document_chunks"

    source_document: Mapped[str] = mapped_column(
        String(150),
        index=True,
        nullable=False,
        comment="Source document identifier (e.g., 'PMEGP_Guidelines', 'MUDRA_Guidelines')",
    )
    chunk_index: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment="Sequential index of this chunk within the source document",
    )
    chunk_text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        comment="The actual text passage (typically 400-600 tokens)",
    )
    page_number: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
        comment="Original PDF page number",
    )
    # pgvector column — 768 dimensions for Gemini text-embedding-004
    embedding = Column(
        Vector(768),
        nullable=True,
        comment="768-dim embedding vector from Gemini text-embedding-004",
    )
    metadata_json: Mapped[Dict[str, Any]] = mapped_column(
        JSON,
        default=dict,
        nullable=False,
        comment="Additional metadata: section title, subsidy rates, etc.",
    )

    __table_args__ = (
        Index("idx_chunk_source_idx", "source_document", "chunk_index", unique=True),
    )
