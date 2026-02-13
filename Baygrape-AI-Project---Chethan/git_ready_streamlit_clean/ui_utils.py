import base64
import mimetypes
import os
import tempfile
from pathlib import Path
from typing import Any

import streamlit as st

from app.main import (
    chroma_clear_api as backend_chroma_clear_api,
    chroma_summary_api as backend_chroma_summary_api,
    query_rag_api as backend_query_rag_api,
    upload_pdf_api as backend_upload_pdf_api,
)

ROOT_DIR = Path(__file__).resolve().parent
STYLE_FILE = ROOT_DIR / "static" / "style.css"
LOADER_FILE = ROOT_DIR / "static" / "loader.css"
def ensure_state() -> None:
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "chroma_loaded" not in st.session_state:
        st.session_state.chroma_loaded = None


def load_css() -> None:
    style_css = STYLE_FILE.read_text(encoding="utf-8")
    loader_css = LOADER_FILE.read_text(encoding="utf-8")
    st.markdown(f"<style>{style_css}\n{loader_css}</style>", unsafe_allow_html=True)


def set_background(image_filename: str) -> None:
    base_dir = os.path.dirname(__file__)
    image_path = os.path.join(base_dir, "background_assets", image_filename)
    path = Path(image_path)
    if not path.exists() or path.stat().st_size == 0:
        st.warning(f"Background image not found: background_assets/{image_filename}")
        return

    mime_type = mimetypes.guess_type(str(path))[0] or "image/jpeg"
    b64 = base64.b64encode(path.read_bytes()).decode("ascii")

    st.markdown(
        f"""
        <style>
        .stApp,
        [data-testid="stAppViewContainer"],
        [data-testid="stHeader"] {{
            background: transparent !important;
        }}

        [data-testid="stAppViewContainer"] {{
            position: relative;
            overflow: hidden;
        }}

        [data-testid="stAppViewContainer"]::before {{
            content: "";
            position: fixed;
            inset: 0;
            z-index: -2;
            background-image: url("data:{mime_type};base64,{b64}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
            transform: scale(1);
            opacity: 1;
            animation: ragFadeIn 0.45s ease-in-out;
        }}

        [data-testid="stAppViewContainer"]::after {{
            content: "";
            position: fixed;
            inset: 0;
            z-index: -1;
            backdrop-filter: blur(0px);
            background: linear-gradient(
                145deg,
                rgba(0, 0, 0, 0.6) 0%,
                rgba(0, 0, 0, 0.65) 60%,
                rgba(0, 0, 0, 0.72) 100%
            );
            pointer-events: none;
        }}

        p, label, span, div, h1, h2, h3, h4 {{
            color: #ecf4ff;
        }}

        @keyframes ragFadeIn {{
            from {{ opacity: 0.25; }}
            to {{ opacity: 1; }}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def show_loader(text: str = "Loading..."):
    placeholder = st.empty()
    placeholder.markdown(
        f"""
        <div class="rag-loader-overlay">
            <div class="rag-loader-core">
                <span class="rag-ring ring-1"></span>
                <span class="rag-ring ring-2"></span>
                <span class="rag-ring ring-3"></span>
                <div class="rag-loader-text">{text}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    return placeholder


def sidebar_nav(active: str) -> None:
    with st.sidebar:
        st.markdown("## RAG Menu")
        st.page_link("app.py", label="Home", icon="🏠")
        st.page_link("pages/embed.py", label="Embed Documents", icon="📄")
        st.page_link("pages/chatbot.py", label="Chatbot", icon="💬")
        st.page_link("pages/chroma_db.py", label="View Chroma DB", icon="🗂️")


def upload_pdf_api(uploaded_file) -> dict[str, Any]:
    if uploaded_file is None:
        raise ValueError("No file provided")

    suffix = Path(uploaded_file.name).suffix or ".pdf"
    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(uploaded_file.getbuffer())
            temp_path = Path(tmp.name)

        return backend_upload_pdf_api(str(temp_path), uploaded_file.name)
    finally:
        if temp_path and temp_path.exists():
            temp_path.unlink(missing_ok=True)


def query_rag_api(question: str) -> dict[str, Any]:
    if not question or not question.strip():
        raise ValueError("Question is required")
    return backend_query_rag_api(question)


def chroma_summary_api(limit: int = 30) -> dict[str, Any]:
    return backend_chroma_summary_api(limit=int(limit))


def chroma_clear_api() -> dict[str, Any]:
    return backend_chroma_clear_api()
