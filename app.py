from __future__ import annotations

import html
from typing import Dict, List

import streamlit as st

try:
    import faiss
    FAISS_IMPORT_ERROR = None
except ImportError as exc:
    faiss = None  # type: ignore[assignment]
    FAISS_IMPORT_ERROR = exc

try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMER_IMPORT_ERROR = None
except ImportError as exc:
    SentenceTransformer = None  # type: ignore[assignment]
    SENTENCE_TRANSFORMER_IMPORT_ERROR = exc

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def inject_styles() -> None:
    st.markdown(
        """
        <style>
            :root {
                --page-bg: #f4efe7;
                --paper: #fffaf4;
                --paper-strong: #fff7ec;
                --ink: #162033;
                --muted: #5e6a79;
                --accent: #0c8d7a;
                --accent-soft: #d8f1eb;
                --warm: #ef8f34;
                --border: rgba(22, 32, 51, 0.08);
                --shadow: 0 20px 55px rgba(20, 35, 52, 0.10);
            }

            .stApp {
                background:
                    radial-gradient(circle at top right, rgba(239, 143, 52, 0.14), transparent 28%),
                    radial-gradient(circle at top left, rgba(12, 141, 122, 0.18), transparent 34%),
                    linear-gradient(180deg, #f4efe7 0%, #f8f4ed 48%, #f3ede5 100%);
                color: var(--ink);
            }

            .block-container {
                max-width: 1180px;
                padding-top: 2.2rem;
                padding-bottom: 3rem;
            }

            h1, h2, h3 {
                font-family: "Trebuchet MS", "Gill Sans", sans-serif;
                color: var(--ink);
                letter-spacing: 0.01em;
            }

            p, li, label, div, span {
                font-family: Georgia, Cambria, serif;
            }

            [data-testid="stMetricValue"] {
                font-family: "Trebuchet MS", "Gill Sans", sans-serif;
            }

            [data-testid="stMetricLabel"],
            [data-testid="stMetricValue"] {
                color: #162033 !important;
            }

            .hero-shell {
                padding: 2rem 2.2rem;
                border-radius: 28px;
                background:
                    linear-gradient(135deg, rgba(12, 141, 122, 0.92), rgba(13, 73, 110, 0.92)),
                    linear-gradient(180deg, rgba(255, 255, 255, 0.12), rgba(255, 255, 255, 0));
                color: #f7fffd;
                box-shadow: var(--shadow);
                position: relative;
                overflow: hidden;
                margin-bottom: 1.6rem;
            }

            .hero-shell::after {
                content: "";
                position: absolute;
                right: -60px;
                top: -60px;
                width: 220px;
                height: 220px;
                background: radial-gradient(circle, rgba(255, 255, 255, 0.22), transparent 72%);
            }

            .hero-kicker {
                text-transform: uppercase;
                letter-spacing: 0.18em;
                font-size: 0.76rem;
                opacity: 0.85;
                margin-bottom: 0.5rem;
                font-family: "Trebuchet MS", "Gill Sans", sans-serif;
            }

            .hero-title {
                font-size: 2.7rem;
                line-height: 1.05;
                margin: 0;
                font-family: "Trebuchet MS", "Gill Sans", sans-serif;
                font-weight: 700;
            }

            .hero-copy {
                max-width: 770px;
                margin-top: 0.9rem;
                font-size: 1.06rem;
                line-height: 1.6;
                color: rgba(247, 255, 253, 0.9);
            }

            .panel-card {
                background: rgba(255, 250, 244, 0.82);
                border: 1px solid var(--border);
                box-shadow: var(--shadow);
                border-radius: 24px;
                padding: 1.3rem 1.35rem;
            }

            .mini-card {
                background: linear-gradient(180deg, rgba(255,255,255,0.85), rgba(255,248,238,0.96));
                border: 1px solid var(--border);
                border-radius: 20px;
                padding: 1rem 1.05rem;
                min-height: 120px;
            }

            .section-label {
                font-family: "Trebuchet MS", "Gill Sans", sans-serif;
                text-transform: uppercase;
                letter-spacing: 0.12em;
                color: var(--muted);
                font-size: 0.78rem;
                margin-bottom: 0.4rem;
            }

            .source-chip {
                display: inline-block;
                margin-top: 0.75rem;
                padding: 0.5rem 0.85rem;
                border-radius: 999px;
                background: rgba(255,255,255,0.18);
                color: #f7fffd;
                border: 1px solid rgba(255,255,255,0.16);
                font-family: "Trebuchet MS", "Gill Sans", sans-serif;
                font-size: 0.85rem;
            }

            .notice {
                background: linear-gradient(90deg, rgba(216, 241, 235, 0.95), rgba(255, 247, 236, 0.95));
                border: 1px solid rgba(12, 141, 122, 0.18);
                color: var(--ink);
                padding: 0.95rem 1rem;
                border-radius: 18px;
                box-shadow: 0 10px 30px rgba(20, 35, 52, 0.06);
                margin-bottom: 1rem;
            }

            .result-card {
                background: linear-gradient(180deg, rgba(255, 250, 244, 0.96), rgba(255, 245, 235, 0.95));
                border: 1px solid rgba(22, 32, 51, 0.08);
                border-left: 8px solid var(--accent);
                border-radius: 24px;
                padding: 1.25rem 1.3rem;
                box-shadow: var(--shadow);
                margin-bottom: 1rem;
            }

            .result-topline {
                display: flex;
                justify-content: space-between;
                gap: 1rem;
                flex-wrap: wrap;
                margin-bottom: 0.85rem;
                align-items: center;
            }

            .result-rank {
                font-family: "Trebuchet MS", "Gill Sans", sans-serif;
                font-size: 0.9rem;
                color: var(--muted);
                text-transform: uppercase;
                letter-spacing: 0.08em;
            }

            .score-pill {
                display: inline-flex;
                gap: 0.55rem;
                align-items: center;
                padding: 0.45rem 0.8rem;
                border-radius: 999px;
                background: rgba(12, 141, 122, 0.10);
                color: var(--accent);
                border: 1px solid rgba(12, 141, 122, 0.14);
                font-family: "Trebuchet MS", "Gill Sans", sans-serif;
            }

            .score-value {
                font-weight: 700;
                font-size: 1rem;
            }

            .result-question {
                font-family: "Trebuchet MS", "Gill Sans", sans-serif;
                font-size: 1.12rem;
                line-height: 1.35;
                font-weight: 700;
                color: var(--ink);
                margin-bottom: 0.65rem;
            }

            .result-answer {
                color: #29364a;
                line-height: 1.7;
                font-size: 1rem;
            }

            .result-footer {
                margin-top: 0.9rem;
                color: var(--muted);
                font-size: 0.9rem;
            }

            .preview-item {
                padding: 0.8rem 0;
                border-bottom: 1px solid rgba(22, 32, 51, 0.08);
            }

            .preview-item:last-child {
                border-bottom: 0;
            }

            .preview-q {
                font-family: "Trebuchet MS", "Gill Sans", sans-serif;
                color: var(--ink);
                margin-bottom: 0.2rem;
            }

            .preview-a {
                color: var(--muted);
            }

            .empty-state {
                padding: 1.3rem 1.2rem;
                border-radius: 22px;
                background: rgba(255, 250, 244, 0.78);
                border: 1px dashed rgba(22, 32, 51, 0.16);
                color: var(--muted);
                box-shadow: inset 0 1px 0 rgba(255,255,255,0.8);
            }

            div[data-testid="stTextInputRootElement"] > div,
            div[data-testid="stNumberInputContainer"] > div,
            div[data-testid="stSelectbox"] > div,
            div[data-testid="stSlider"] {
                background: rgba(255, 255, 255, 0.65);
                border-radius: 16px;
            }

            .stButton > button {
                border-radius: 14px;
                border: 1px solid rgba(22, 32, 51, 0.10);
                padding: 0.65rem 1rem;
                font-family: "Trebuchet MS", "Gill Sans", sans-serif;
                font-weight: 600;
                box-shadow: 0 10px 28px rgba(20, 35, 52, 0.07);
            }

            .stButton > button[kind="primary"] {
                background: linear-gradient(135deg, #0c8d7a, #0d496e);
                color: #ffffff;
            }

            div[data-testid="stFileUploader"] label,
            div[data-testid="stFileUploader"] small,
            div[data-testid="stFileUploader"] span,
            div[data-testid="stFileUploader"] p {
                color: #fffaf4 !important;
            }

            div[data-testid="stFileUploaderDropzone"] {
                background: rgba(255, 250, 244, 0.96) !important;
                border: 1px solid rgba(22, 32, 51, 0.12) !important;
                border-radius: 18px !important;
            }

            div[data-testid="stFileUploaderDropzone"] button {
                background: linear-gradient(135deg, #0c8d7a, #0d496e) !important;
                color: #ffffff !important;
                border: 0 !important;
            }

            div[data-testid="stFileUploaderDropzone"] small,
            div[data-testid="stFileUploaderDropzone"] span,
            div[data-testid="stFileUploaderDropzone"] p,
            div[data-testid="stFileUploaderDropzoneInstructions"] {
                color: #162033 !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_hero(entries_count: int, source_name: str | None) -> None:
    source_label = source_name if source_name else "Upload a file to begin"
    st.markdown(
        f"""
        <section class="hero-shell">
            <div class="hero-kicker">SentenceTransformer + FAISS</div>
            <h1 class="hero-title">Document Semantic Search</h1>
            <div class="hero-copy">
                Upload a document, convert its question-answer pairs into embeddings, and search it with semantic similarity
                instead of plain keyword matching. The engine reads one uploaded source file, indexes it with FAISS, and returns the
                most relevant answers in a cleaner, more structured layout.
            </div>
            <div class="source-chip">Source file: {html.escape(source_label)} | Loaded pairs: {entries_count}</div>
        </section>
        """,
        unsafe_allow_html=True,
    )


@st.cache_data(show_spinner=False)
def decode_uploaded_text(file_bytes: bytes) -> str:
    for encoding in ("utf-8", "utf-8-sig", "latin-1"):
        try:
            return file_bytes.decode(encoding)
        except UnicodeDecodeError:
            continue
    raise ValueError("The uploaded file could not be decoded as text.")


@st.cache_data(show_spinner=False)
def load_entries_from_text(document_text: str) -> List[Dict[str, str]]:
    cleaned_lines = [line.strip() for line in document_text.splitlines() if line.strip()]

    if len(cleaned_lines) % 2 != 0:
        raise ValueError(
            "The document should contain alternating question and answer lines. "
            f"Found {len(cleaned_lines)} non-empty lines."
        )

    entries: List[Dict[str, str]] = []
    for index in range(0, len(cleaned_lines), 2):
        question = cleaned_lines[index]
        answer = cleaned_lines[index + 1]
        entries.append(
            {
                "pair_id": str((index // 2) + 1),
                "question": question,
                "answer": answer,
                "combined": f"Question: {question}\nAnswer: {answer}",
            }
        )
    return entries


@st.cache_resource(show_spinner=True)
def build_search_assets(document_text: str) -> Dict[str, object]:
    entries = load_entries_from_text(document_text)
    model = SentenceTransformer(MODEL_NAME)
    embeddings = model.encode(
        [entry["combined"] for entry in entries],
        convert_to_numpy=True,
        normalize_embeddings=True,
    ).astype("float32")

    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)
    return {"entries": entries, "model": model, "index": index}


def semantic_search(query: str, top_k: int, document_text: str) -> List[Dict[str, object]]:
    assets = build_search_assets(document_text)
    model: SentenceTransformer = assets["model"]  # type: ignore[assignment]
    index: faiss.IndexFlatIP = assets["index"]  # type: ignore[assignment]
    entries: List[Dict[str, str]] = assets["entries"]  # type: ignore[assignment]

    query_embedding = model.encode(
        [query],
        convert_to_numpy=True,
        normalize_embeddings=True,
    ).astype("float32")

    limit = min(top_k, len(entries))
    scores, indices = index.search(query_embedding, limit)

    results: List[Dict[str, object]] = []
    for score, index_position in zip(scores[0], indices[0]):
        entry = entries[int(index_position)]
        semantic_percent = max(0.0, min(1.0, float(score))) * 100
        results.append(
            {
                "pair_id": entry["pair_id"],
                "question": entry["question"],
                "answer": entry["answer"],
                "score": float(score),
                "semantic_percent": semantic_percent,
            }
        )
    return results


def render_dataset_panel(entries: List[Dict[str, str]], source_name: str | None) -> None:
    preview_markup = []
    for entry in entries[:3]:
        preview_markup.append(
            f"""
            <div class="preview-item">
                <div class="preview-q">{html.escape(entry["question"])}</div>
                <div class="preview-a">{html.escape(entry["answer"])}</div>
            </div>
            """
        )

    st.markdown("### Document Overview")
    st.caption("One uploaded file is indexed at a time.")

    metric_col_1, metric_col_2 = st.columns(2)
    metric_col_1.metric("Q&A pairs", len(entries))
    metric_col_2.metric("Search backend", "FAISS")

    st.markdown(
        """
        <div class="mini-card" style="margin-top: 0.8rem;">
            <div class="section-label">Source file</div>
            <div style="font-size: 0.98rem; line-height: 1.6; color: var(--ink);">
                {source_name}
            </div>
        </div>
        """.replace("{source_name}", html.escape(source_name or "No file uploaded")),
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="mini-card" style="margin-top: 0.9rem;">
            <div class="section-label">Detected format</div>
            <div style="line-height: 1.7; color: var(--muted);">
                The file is parsed as alternating lines:
                question, answer, question, answer.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="mini-card" style="margin-top: 0.9rem;">
            <div class="section-label">Preview</div>
            {''.join(preview_markup)}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_result_card(result: Dict[str, object], rank: int) -> None:
    st.markdown(
        f"""
        <div class="result-card">
            <div class="result-topline">
                <div class="result-rank">Top match {rank} | Pair {html.escape(str(result["pair_id"]))}</div>
                <div class="score-pill">
                    <span>Semantic match</span>
                    <span class="score-value">{result["semantic_percent"]:.1f}%</span>
                    <span>| cosine {result["score"]:.4f}</span>
                </div>
            </div>
            <div class="result-question">{html.escape(str(result["question"]))}</div>
            <div class="result-answer">{html.escape(str(result["answer"]))}</div>
            <div class="result-footer">Retrieved from the uploaded document using SentenceTransformer embeddings and FAISS inner-product search.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def main() -> None:
    st.set_page_config(
        page_title="Semantic Search Engine",
        layout="wide",
    )
    inject_styles()

    if "query_text" not in st.session_state:
        st.session_state["query_text"] = ""
    if "active_query" not in st.session_state:
        st.session_state["active_query"] = ""
    if "active_top_k" not in st.session_state:
        st.session_state["active_top_k"] = 4
    if "active_document_text" not in st.session_state:
        st.session_state["active_document_text"] = ""
    if "active_source_name" not in st.session_state:
        st.session_state["active_source_name"] = ""

    if FAISS_IMPORT_ERROR or SENTENCE_TRANSFORMER_IMPORT_ERROR:
        st.error(
            "Missing dependencies in the current Python interpreter. "
            "Use Python 3.11 for this project and run `install_requirements.ps1`, "
            "then start the app with `run_app.ps1`."
        )
        if FAISS_IMPORT_ERROR:
            st.code(f"FAISS import error: {FAISS_IMPORT_ERROR}")
        if SENTENCE_TRANSFORMER_IMPORT_ERROR:
            st.code(f"SentenceTransformer import error: {SENTENCE_TRANSFORMER_IMPORT_ERROR}")
        return

    uploaded_file = st.file_uploader(
        "Upload your document",
        type=None,
        help="Upload a text-based file formatted as alternating question and answer lines.",
    )

    entries: List[Dict[str, str]] = []
    uploaded_text = ""
    uploaded_name = uploaded_file.name if uploaded_file else None

    if uploaded_file is not None:
        try:
            uploaded_text = decode_uploaded_text(uploaded_file.getvalue())
            entries = load_entries_from_text(uploaded_text)
            if (
                st.session_state["active_source_name"] != (uploaded_name or "")
                or st.session_state["active_document_text"] != uploaded_text
            ):
                st.session_state["active_query"] = ""
        except Exception as exc:
            st.error(str(exc))
            return
    else:
        st.session_state["active_document_text"] = ""
        st.session_state["active_source_name"] = ""

    render_hero(len(entries), uploaded_name)

    st.markdown(
        f"""
        <div class="notice">
            Upload one document, index its question-answer pairs, and search only within that file.
        </div>
        """,
        unsafe_allow_html=True,
    )

    left_col, right_col = st.columns([0.95, 1.35], gap="large")

    with left_col:
        st.markdown('<div class="panel-card">', unsafe_allow_html=True)
        st.markdown("### Upload Dataset")
        st.caption("Use one uploaded file at a time. The app reads alternating question and answer lines.")
        if uploaded_file is not None:
            render_dataset_panel(entries, uploaded_name)
        else:
            st.markdown(
                """
                <div class="empty-state">
                    Upload any text-based file to build the semantic search index. Once uploaded, you can ask questions
                    and retrieve the closest answers from that file.
                </div>
                """,
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)

    with right_col:
        st.markdown('<div class="panel-card">', unsafe_allow_html=True)
        st.markdown("### Search Query")
        st.caption("Ask naturally. Semantic search will find the closest answer inside the uploaded file even if wording changes.")

        sample_questions = [
            "What is the office working time?",
            "How many paid leaves do we get in a year?",
            "Can I work from home during the week?",
            "How do I contact HR?",
        ]

        sample_cols = st.columns(2, gap="small")
        sample_clicked = False
        for position, sample in enumerate(sample_questions):
            with sample_cols[position % 2]:
                if st.button(sample, key=f"sample_{position}", use_container_width=True):
                    st.session_state["query_text"] = sample
                    sample_clicked = True

        st.text_input(
            "Enter your question",
            key="query_text",
            placeholder="Example: What is the office working time?",
        )
        if entries:
            top_k = st.slider(
                "Number of top results",
                min_value=1,
                max_value=min(8, len(entries)),
                value=min(4, len(entries)),
            )
        else:
            top_k = 3
            st.slider(
                "Number of top results",
                min_value=1,
                max_value=8,
                value=3,
                disabled=True,
            )
        search_clicked = st.button("Search answers", type="primary", use_container_width=True)

        if search_clicked or sample_clicked:
            st.session_state["active_query"] = st.session_state["query_text"].strip()
            st.session_state["active_top_k"] = top_k
            st.session_state["active_document_text"] = uploaded_text
            st.session_state["active_source_name"] = uploaded_name or ""

        st.markdown("</div>", unsafe_allow_html=True)

    active_query = st.session_state["active_query"]
    active_top_k = int(st.session_state["active_top_k"])
    active_document_text = st.session_state["active_document_text"]
    active_source_name = st.session_state["active_source_name"]

    st.markdown("### Top Search Results")

    if active_query and active_document_text:
        with st.spinner("Finding the closest answers..."):
            try:
                results = semantic_search(active_query, active_top_k, active_document_text)
            except Exception as exc:
                st.error(f"Search failed: {exc}")
                return

        st.caption(f'Query: "{active_query}" | File: "{active_source_name}"')
        for rank, result in enumerate(results, start=1):
            render_result_card(result, rank)
    else:
        st.markdown(
            """
            <div class="empty-state">
                Upload a document first, then enter a question or click one of the sample prompts to see ranked semantic matches.
            </div>
            """,
            unsafe_allow_html=True,
        )


if __name__ == "__main__":
    main()
