import chromadb
from app.config import CHROMA_DB_DIR


def get_chroma_client():
    """
    Use local persistent Chroma storage for single-app Streamlit deployments.
    """
    return chromadb.PersistentClient(path=CHROMA_DB_DIR)
