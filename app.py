"""
Streamlit UI for the Multi-Agent Research System.

Drop this file in the same folder as pipeline.py, agents.py and tool.py
(i.e. next to them, NOT inside .venv/), then run:

    streamlit run app.py

It imports `run_research_pipeline` from pipeline.py, runs it in a background
thread so the UI stays responsive, and streams the console logs your
pipeline already prints straight into the page — so you get a "live" view
of Search -> Read -> Write -> Critique without touching your agent logic.
"""

import io
import os
import sys
import queue
import threading
import contextlib
import traceback
from datetime import datetime

import streamlit as st

# ---------------------------------------------------------------------------
# Page setup
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Multi-Agent Research System",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .stApp { background-color: #0e1117; }
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #7C3AED, #06B6D4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
    }
    .subtitle { color: #9CA3AF; margin-top: 0.2rem; margin-bottom: 1.4rem; }
    .agent-badge {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 999px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-right: 6px;
    }
    .badge-search { background:#1E3A8A33; color:#60A5FA; border:1px solid #60A5FA55; }
    .badge-read   { background:#78350F33; color:#FBBF24; border:1px solid #FBBF2455; }
    .badge-write  { background:#14532D33; color:#4ADE80; border:1px solid #4ADE8055; }
    .badge-critic { background:#7F1D1D33; color:#F87171; border:1px solid #F8717155; }
    .log-box {
        background:#0b0d12;
        border:1px solid #262b36;
        border-radius:8px;
        padding:12px 14px;
        font-family:'JetBrains Mono','Courier New',monospace;
        font-size:0.82rem;
        color:#c9d1d9;
        white-space:pre-wrap;
        max-height:340px;
        overflow-y:auto;
    }
    .report-card {
        background:#11151c;
        border:1px solid #262b36;
        border-radius:12px;
        padding:1.4rem 1.6rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Import the pipeline (fail loudly but gracefully in the UI, not a crash)
# ---------------------------------------------------------------------------
IMPORT_ERROR = None
try:
    from pipeline import run_research_pipeline
except Exception as e:  # noqa: BLE001
    IMPORT_ERROR = e

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass


def extract_text(value) -> str:
    """LangChain chains/objects sometimes return AIMessage, sometimes str."""
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    content = getattr(value, "content", None)
    if isinstance(content, str):
        return content
    return str(value)


def run_pipeline_threaded(topic: str, log_q: "queue.Queue", result_box: dict):
    """Runs the blocking pipeline in a worker thread, forwarding stdout live."""

    class QueueWriter(io.TextIOBase):
        def write(self, s):
            if s:
                log_q.put(s)
            return len(s)

        def flush(self):
            pass

    try:
        with contextlib.redirect_stdout(QueueWriter()):
            state = run_research_pipeline(topic)
        result_box["state"] = state
    except Exception as e:  # noqa: BLE001
        result_box["error"] = f"{e}\n\n{traceback.format_exc()}"
    finally:
        log_q.put("__PIPELINE_DONE__")


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🧠 Research System")
    st.caption("Search agent → Reader agent → Writer chain → Critic chain")

    st.divider()
    st.markdown("**Environment**")
    env_keys_present = any(
        os.environ.get(k)
        for k in ("OPENAI_API_KEY", "ANTHROPIC_API_KEY", "TAVILY_API_KEY", "GOOGLE_API_KEY")
    )
    st.write("🔑 `.env` keys detected" if env_keys_present else "⚠️ No known API keys found in environment")

    st.divider()
    st.markdown("**History**")
    if "history" not in st.session_state:
        st.session_state.history = []
    if st.session_state.history:
        for h in reversed(st.session_state.history[-10:]):
            st.caption(f"• {h}")
    else:
        st.caption("No runs yet this session.")

    st.divider()
    st.caption("Built on your `pipeline.py` — logic untouched, UI only.")

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.markdown('<p class="main-title">Multi-Agent Research Assistant</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="subtitle">Give it a topic — a search agent, reader agent, writer and critic '
    "collaborate to produce a reviewed research report.</p>",
    unsafe_allow_html=True,
)

if IMPORT_ERROR is not None:
    st.error(
        "Couldn't import `run_research_pipeline` from pipeline.py.\n\n"
        f"**{type(IMPORT_ERROR).__name__}:** {IMPORT_ERROR}\n\n"
        "Make sure `app.py` sits in the same folder as `pipeline.py`, `agents.py` "
        "and `tool.py` (not inside `.venv/`), and that all packages in "
        "`requirements.txt` are installed."
    )
    st.stop()

# ---------------------------------------------------------------------------
# Input row
# ---------------------------------------------------------------------------
col1, col2 = st.columns([5, 1])
with col1:
    topic = st.text_input(
        "Research topic",
        placeholder="e.g. Impact of quantum computing on cryptography in 2026",
        label_visibility="collapsed",
    )
with col2:
    start = st.button("🚀 Research", use_container_width=True, type="primary")

# ---------------------------------------------------------------------------
# Run pipeline
# ---------------------------------------------------------------------------
if start:
    if not topic or not topic.strip():
        st.warning("Please enter a topic first.")
        st.stop()

    st.session_state.history.append(topic.strip())

    log_q: "queue.Queue" = queue.Queue()
    result_box: dict = {}

    worker = threading.Thread(
        target=run_pipeline_threaded, args=(topic.strip(), log_q, result_box), daemon=True
    )
    worker.start()

    status_placeholder = st.empty()
    log_placeholder = st.empty()

    steps = [
        ("search", "badge-search", "🔎 Search agent"),
        ("reader", "badge-read", "📖 Reader agent"),
        ("writer", "badge-write", "✍️ Writer"),
        ("critic", "badge-critic", "🧐 Critic"),
    ]
    step_keywords = {
        "search": "step 1",
        "reader": "step 2",
        "writer": "step 3",
        "critic": "step 4",
    }
    current_step = "search"

    log_text = ""
    while True:
        try:
            chunk = log_q.get(timeout=0.2)
        except queue.Empty:
            continue

        if chunk == "__PIPELINE_DONE__":
            break

        log_text += chunk
        lowered = log_text.lower()
        for key, kw in step_keywords.items():
            if kw in lowered:
                current_step = key

        badges = "".join(
            f'<span class="agent-badge {cls}">{"✅ " if step_keywords[key] in log_text.lower() and key != current_step else ("🔄 " if key == current_step else "⏳ ")}{label}</span>'
            for key, cls, label in steps
        )
        status_placeholder.markdown(badges, unsafe_allow_html=True)
        log_placeholder.markdown(
            f'<div class="log-box">{log_text[-4000:]}</div>', unsafe_allow_html=True
        )

    worker.join()

    if "error" in result_box:
        st.error("The pipeline raised an error:")
        st.code(result_box["error"])
        st.stop()

    state = result_box.get("state", {})
    report_text = extract_text(state.get("report"))
    feedback_text = extract_text(state.get("feedback"))

    st.success(f"Research complete — {datetime.now().strftime('%H:%M:%S')}")

    tabs = st.tabs(["📄 Report", "🧐 Critic feedback", "🔎 Search results", "📖 Scraped content"])

    with tabs[0]:
        st.markdown('<div class="report-card">', unsafe_allow_html=True)
        st.markdown(report_text if report_text else "_No report produced._")
        st.markdown("</div>", unsafe_allow_html=True)
        if report_text:
            st.download_button(
                "⬇️ Download report (.md)",
                data=report_text,
                file_name=f"research_report_{topic.strip().replace(' ', '_')[:40]}.md",
                mime="text/markdown",
            )

    with tabs[1]:
        st.markdown(feedback_text if feedback_text else "_No feedback produced._")

    with tabs[2]:
        st.text(state.get("search_results", "No search results captured."))

    with tabs[3]:
        st.text(state.get("scraped_content", "No scraped content captured."))