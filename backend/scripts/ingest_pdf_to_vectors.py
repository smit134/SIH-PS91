"""Ingest PMEGP/MUDRA PDF Guidelines into pgvector for RAG retrieval.

Usage:
    python -m scripts.ingest_pdf_to_vectors [--pdf data/raw/pdfs/pmegp_guidelines.pdf] [--dry-run]

Downloads:
    PMEGP: https://www.kviconline.gov.in/pmegp/pmegpweb/docs/homepage/PMEGPscheme.pdf
    MUDRA: https://www.mudra.org.in/
"""

import json
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import asyncio
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_sessionmaker, get_engine, Base
from app.models.document_chunk import SchemeDocumentChunk


# --- PDF Text Extraction ---
def extract_text_from_pdf(pdf_path: str) -> list:
    """Extract text from PDF, returning list of (page_number, text) tuples."""
    try:
        from PyPDF2 import PdfReader
    except ImportError:
        print("ERROR: PyPDF2 not installed. Run: pip install PyPDF2")
        sys.exit(1)
    
    reader = PdfReader(pdf_path)
    pages = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text and text.strip():
            pages.append((i + 1, text.strip()))
    
    print(f"  Extracted text from {len(pages)} pages")
    return pages


# --- Text Chunking ---
def chunk_text(pages: list, chunk_size: int = 500, overlap: int = 50) -> list:
    """
    Split extracted pages into overlapping chunks of ~chunk_size words.
    Returns list of dicts: {chunk_index, chunk_text, page_number}.
    """
    chunks = []
    chunk_index = 0
    
    for page_num, page_text in pages:
        words = page_text.split()
        
        i = 0
        while i < len(words):
            end = min(i + chunk_size, len(words))
            chunk_words = words[i:end]
            chunk_text = " ".join(chunk_words)
            
            if len(chunk_text.strip()) > 50:  # Skip very short chunks
                chunks.append({
                    "chunk_index": chunk_index,
                    "chunk_text": chunk_text,
                    "page_number": page_num,
                })
                chunk_index += 1
            
            i += chunk_size - overlap
            if i >= len(words):
                break
    
    print(f"  Created {len(chunks)} text chunks (size={chunk_size}, overlap={overlap})")
    return chunks


# --- Gemini Embedding ---
def get_gemini_embedding(text: str, api_key: str) -> list:
    """Generate a 768-dim embedding using Gemini text-embedding-004."""
    from google import genai
    
    client = genai.Client(api_key=api_key)
    
    # Truncate text to 2048 tokens max (approximately 8000 chars)
    truncated = text[:8000]
    
    result = client.models.embed_content(
        model="text-embedding-004",
        contents=truncated,
    )
    
    return result.embeddings[0].values


def get_gemini_embeddings_batch(texts: list, api_key: str, batch_size: int = 20) -> list:
    """Generate embeddings for a batch of texts with rate limiting."""
    all_embeddings = []
    
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        print(f"    Embedding batch {i // batch_size + 1}/{(len(texts) + batch_size - 1) // batch_size}...")
        
        for text in batch:
            try:
                emb = get_gemini_embedding(text, api_key)
                all_embeddings.append(emb)
            except Exception as e:
                print(f"    WARN: Embedding failed: {e}")
                all_embeddings.append([0.0] * 768)  # Zero vector fallback
            
            time.sleep(0.1)  # Rate limiting: 10 req/s for free tier
        
        # Extra pause between batches
        if i + batch_size < len(texts):
            time.sleep(1.0)
    
    return all_embeddings


async def enable_pgvector(engine):
    """Ensure pgvector extension is enabled."""
    async with engine.begin() as conn:
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
    print("  pgvector extension enabled")


async def ingest_pdf(pdf_path: str, source_name: str, dry_run: bool = False):
    """Main PDF → pgvector ingestion pipeline."""
    print("=" * 60)
    print(f"ThinkForge — PDF RAG Ingestion: {source_name}")
    print("=" * 60)
    
    pdf_file = Path(pdf_path)
    if not pdf_file.exists():
        print(f"  ERROR: PDF not found: {pdf_file}")
        print(f"  Download it first:")
        print(f"    For PMEGP: curl -o {pdf_path} https://www.kviconline.gov.in/pmegp/pmegpweb/docs/homepage/PMEGPscheme.pdf")
        return
    
    # Step 1: Extract text
    pages = extract_text_from_pdf(str(pdf_file))
    
    # Step 2: Chunk
    chunks = chunk_text(pages, chunk_size=500, overlap=50)
    
    if dry_run:
        print("\n--- DRY RUN ---")
        for c in chunks[:5]:
            preview = c["chunk_text"][:100].replace("\n", " ")
            print(f"  Chunk {c['chunk_index']:3d} (page {c['page_number']:2d}): {preview}...")
        print(f"  ... and {len(chunks) - 5} more chunks")
        return
    
    # Step 3: Get API key
    from app.config import settings
    api_key = settings.GEMINI_API_KEY
    if not api_key or api_key == "redacted":
        api_key = os.environ.get("GEMINI_API_KEY", "")
    
    if not api_key:
        print("  ERROR: GEMINI_API_KEY not set. Cannot generate embeddings.")
        print("  Set it in backend/.env or as an environment variable.")
        return
    
    # Step 4: Generate embeddings
    print("\n  Generating embeddings via Gemini text-embedding-004...")
    texts = [c["chunk_text"] for c in chunks]
    embeddings = get_gemini_embeddings_batch(texts, api_key)
    
    # Step 5: Store in DB
    engine = get_engine()
    await enable_pgvector(engine)
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    sessionmaker = get_sessionmaker()
    async with sessionmaker() as db:
        inserted = 0
        for chunk, embedding in zip(chunks, embeddings):
            # Check duplicate
            existing = await db.execute(
                select(SchemeDocumentChunk).where(
                    SchemeDocumentChunk.source_document == source_name,
                    SchemeDocumentChunk.chunk_index == chunk["chunk_index"],
                )
            )
            if existing.scalar_one_or_none():
                continue
            
            doc_chunk = SchemeDocumentChunk(
                source_document=source_name,
                chunk_index=chunk["chunk_index"],
                chunk_text=chunk["chunk_text"],
                page_number=chunk["page_number"],
                embedding=embedding,
                metadata_json={
                    "pdf_source": str(pdf_file.name),
                    "word_count": len(chunk["chunk_text"].split()),
                },
            )
            db.add(doc_chunk)
            inserted += 1
        
        await db.commit()
        print(f"\n  DONE: Inserted {inserted} vectorized chunks for '{source_name}'")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Ingest PDF guidelines into pgvector for RAG")
    parser.add_argument("--pdf", default="data/raw/pdfs/pmegp_guidelines.pdf", help="Path to PDF file")
    parser.add_argument("--source-name", default="PMEGP_Guidelines", help="Source document identifier")
    parser.add_argument("--dry-run", action="store_true", help="Extract and chunk without DB writes")
    args = parser.parse_args()
    
    asyncio.run(ingest_pdf(args.pdf, args.source_name, dry_run=args.dry_run))
