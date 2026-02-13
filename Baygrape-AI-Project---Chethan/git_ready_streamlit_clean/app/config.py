import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = st.secrets["GEMINI_API_KEY"]
CHROMA_DB_DIR = os.getenv("CHROMA_DB_DIR", "./chroma_store")
COLLECTION_NAME = "rag_documents"
