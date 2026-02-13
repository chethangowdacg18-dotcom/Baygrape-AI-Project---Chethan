import streamlit as st

from ui_utils import (
    chroma_clear_api,
    chroma_summary_api,
    ensure_state,
    load_css,
    set_background,
    show_loader,
    sidebar_nav,
)


def render_chroma() -> None:
    st.set_page_config(page_title="Chroma DB", page_icon="🗂️", layout="wide")
    ensure_state()
    load_css()
    set_background("chroma.avif")
    sidebar_nav("View Chroma DB")

    st.markdown('<h1 class="page-title">Chroma DB</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="page-subtitle">Inspect vectors, source files, and chunk previews stored in Chroma.</p>',
        unsafe_allow_html=True,
    )

    top_left, top_right = st.columns(2)
    with top_left:
        load_clicked = st.button("Load Database Summary", use_container_width=True)
    with top_right:
        clear_clicked = st.button("Clear Collection", use_container_width=True)

    if clear_clicked:
        loader = show_loader("Clearing...")
        try:
            chroma_clear_api()
            st.session_state.chroma_loaded = None
            st.success("Collection cleared.")
        except Exception as exc:
            st.error(f"Clear failed: {exc}")
        finally:
            loader.empty()

    if load_clicked or st.session_state.chroma_loaded is None:
        loader = show_loader("Loading...")
        try:
            st.session_state.chroma_loaded = chroma_summary_api(limit=40)
        except Exception as exc:
            st.error(f"Load failed: {exc}")
        finally:
            loader.empty()

    data = st.session_state.chroma_loaded
    if data:
        m1, m2, m3 = st.columns(3)
        m1.metric("Vectors", data.get("vector_count", 0))
        m2.metric("Sources", data.get("source_count", 0))
        m3.metric("Avg chars/chunk", data.get("avg_chunk_chars", 0.0))

        st.markdown(
            f'<div class="chip-muted">Collection: {data.get("collection_name", "unknown")}</div>',
            unsafe_allow_html=True,
        )

        sources = data.get("sources", [])
        if sources:
            st.markdown('<h3 class="section-title">Sources</h3>', unsafe_allow_html=True)
            st.write(", ".join(sources))
        else:
            st.info("No sources found.")

        st.markdown('<h3 class="section-title">Chunk Preview</h3>', unsafe_allow_html=True)
        preview_rows = data.get("preview_rows", [])
        if preview_rows:
            st.dataframe(preview_rows, use_container_width=True, hide_index=True)
        else:
            st.info("No chunk rows available.")


render_chroma()
