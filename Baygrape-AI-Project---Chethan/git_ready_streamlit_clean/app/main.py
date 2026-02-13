from app.config import COLLECTION_NAME
from app.ingestion.ingest import ingest_pdf
from app.ingestion.pdf_loader import load_and_split_pdf
from app.rag.chroma_client import get_chroma_client
from app.rag.pipeline import rag_pipeline
from app.rag.vectorstore import get_collection


def upload_pdf_api(file_path: str, source_name: str) -> dict:
    text_chunks = load_and_split_pdf(file_path)
    ingest_pdf(text_chunks=text_chunks, source=source_name)
    return {
        "status": "PDF ingested successfully",
        "source": source_name,
        "chunks_ingested": len(text_chunks),
    }


def query_rag_api(question: str) -> dict:
    return {"answer": rag_pipeline(question)}


def chroma_summary_api(limit: int = 20) -> dict:
    safe_limit = max(1, min(limit, 200))
    collection = get_collection()
    count = collection.count()
    records = collection.get(include=["documents", "metadatas"])

    ids = records.get("ids", [])
    documents = records.get("documents", [])
    metadatas = records.get("metadatas", [])

    sources = sorted(
        {md.get("source", "unknown") for md in metadatas if isinstance(md, dict)}
    )

    preview_rows = []
    total_chars = 0
    for idx, doc in enumerate(documents):
        text = doc or ""
        total_chars += len(text)
        source = "unknown"
        if idx < len(metadatas) and isinstance(metadatas[idx], dict):
            source = metadatas[idx].get("source", "unknown")
        preview_rows.append(
            {
                "id": ids[idx] if idx < len(ids) else f"row-{idx}",
                "source": source,
                "chars": len(text),
                "preview": text[:240],
            }
        )

    avg_chunk_chars = (total_chars / len(documents)) if documents else 0.0
    return {
        "collection_name": COLLECTION_NAME,
        "vector_count": count,
        "source_count": len(sources),
        "sources": sources,
        "avg_chunk_chars": round(avg_chunk_chars, 2),
        "preview_rows": preview_rows[:safe_limit],
    }


def chroma_clear_api() -> dict:
    client = get_chroma_client()
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass
    client.get_or_create_collection(COLLECTION_NAME)
    return {"status": "cleared", "collection_name": COLLECTION_NAME}
