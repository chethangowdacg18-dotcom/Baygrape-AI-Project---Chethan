import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = (
    st.secrets.get("GEMINI_API_KEY")
    if hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets
    else os.getenv("GOOGLE_API_KEY")
)
CHROMA_DB_DIR = os.getenv("CHROMA_DB_DIR", "./chroma_store")
COLLECTION_NAME = "rag_documents"
