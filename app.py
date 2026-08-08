"""
BuildMate AI — Streamlit UI
----------------------------
This file contains ONLY the UI layer. All LangGraph logic (state, nodes,
prompts, Groq initialization, and the compiled graph) lives in project.py
and is imported here, not duplicated.

Run with:  streamlit run app.py
"""

import html as htmllib

import markdown as md
import streamlit as st

from project import app as workflow_app  # the compiled LangGraph graph


# ------------------------------------------------------------------
# Page config
# ------------------------------------------------------------------
st.set_page_config(
    page_title="BuildMate AI",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ------------------------------------------------------------------
# Cached workflow runner
# ------------------------------------------------------------------
@st.cache_resource
def get_workflow():
    """Return the compiled LangGraph app (cached across reruns)."""
    return workflow_app


def run_workflow(query: str) -> dict:
    graph = get_workflow()
    initial_state = {"query": query, "info": {}}
    result = graph.invoke(initial_state)
    return result["info"]


def md_to_html(text: str) -> str:
    """Convert generated Markdown to HTML for embedding inside a styled card."""
    return md.markdown(text, extensions=["fenced_code", "tables", "nl2br"])


# ------------------------------------------------------------------
# Styling — dark, glassmorphic, SaaS-product aesthetic
# ------------------------------------------------------------------
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        .stApp {
            background: radial-gradient(circle at 15% 0%, #1a1533 0%, #0b0c14 45%, #08090f 100%);
            color: #e6e6f0;
        }

        #MainMenu, footer, header {visibility: hidden;}

        .block-container {
            padding-top: 2.5rem;
            padding-bottom: 4rem;
            max-width: 980px;
        }

        /* ---------- Hero ---------- */
        .hero-wrap {
            text-align: center;
            padding: 2.5rem 1rem 2rem 1rem;
            margin-bottom: 1.5rem;
        }
        .hero-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            padding: 0.35rem 0.9rem;
            border-radius: 999px;
            background: rgba(139, 124, 246, 0.10);
            border: 1px solid rgba(139, 124, 246, 0.35);
            color: #b7a9ff;
            font-size: 0.78rem;
            font-weight: 500;
            letter-spacing: 0.03em;
            margin-bottom: 1.1rem;
        }
        .hero-title {
            font-size: 3.2rem;
            font-weight: 800;
            letter-spacing: -0.03em;
            line-height: 1.05;
            margin: 0;
            background: linear-gradient(135deg, #ffffff 20%, #b7a9ff 65%, #8b7cf6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        .hero-tagline {
            font-size: 1.15rem;
            font-weight: 600;
            color: #8b7cf6;
            margin-top: 0.6rem;
            letter-spacing: 0.01em;
        }
        .hero-desc {
            font-size: 1.02rem;
            color: #9a9ab0;
            max-width: 620px;
            margin: 1rem auto 0 auto;
            line-height: 1.6;
            font-weight: 400;
        }

        /* ---------- Glass card (used for input container AND output cards) ---------- */
        .glass-card,
        div[data-testid="stVerticalBlockBorderWrapper"] {
            background: rgba(255, 255, 255, 0.035) !important;
            border: 1px solid rgba(255, 255, 255, 0.09) !important;
            border-radius: 18px !important;
            backdrop-filter: blur(18px);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.25);
        }
        .glass-card {
            padding: 1.75rem 1.9rem;
            margin-bottom: 1.6rem;
        }
        div[data-testid="stVerticalBlockBorderWrapper"] {
            padding: 0.4rem 0.6rem 0.9rem 0.6rem;
            margin-bottom: 1.6rem;
        }

        .section-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 0.25rem;
        }
        .section-title {
            font-size: 1.25rem;
            font-weight: 700;
            color: #f2f2fa;
            margin: 0;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        .section-subtitle {
            font-size: 0.92rem;
            color: #8d8da3;
            margin: 0.15rem 0 1.1rem 0;
            font-weight: 400;
        }
        .section-icon {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 34px;
            height: 34px;
            border-radius: 10px;
            font-size: 1rem;
            background: linear-gradient(135deg, rgba(139,124,246,0.25), rgba(139,124,246,0.05));
            border: 1px solid rgba(139,124,246,0.3);
        }

        .output-box {
            background: rgba(0, 0, 0, 0.28);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 12px;
            padding: 1.2rem 1.4rem;
            max-height: 480px;
            overflow-y: auto;
        }
        .output-box p, .output-box li { color: #d4d4e2; line-height: 1.65; }
        .output-box h1, .output-box h2, .output-box h3 { color: #f2f2fa; }
        .output-box code {
            background: rgba(139,124,246,0.12);
            color: #c9bdff;
            padding: 0.1rem 0.35rem;
            border-radius: 5px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.85em;
        }
        .output-box pre {
            background: rgba(0,0,0,0.35) !important;
            border: 1px solid rgba(255,255,255,0.07);
            border-radius: 10px;
            padding: 0.8rem 1rem;
            overflow-x: auto;
        }

        /* ---------- Input area ---------- */
        .stTextArea textarea {
            background: rgba(255, 255, 255, 0.035) !important;
            border: 1px solid rgba(255, 255, 255, 0.10) !important;
            border-radius: 14px !important;
            color: #eaeaf4 !important;
            font-size: 0.98rem !important;
            padding: 1rem !important;
            line-height: 1.6 !important;
        }
        .stTextArea textarea:focus {
            border-color: rgba(139, 124, 246, 0.55) !important;
            box-shadow: 0 0 0 3px rgba(139, 124, 246, 0.12) !important;
        }
        .stTextArea textarea::placeholder { color: #6b6b80 !important; }

        /* ---------- Button ---------- */
        .stButton > button {
            width: 100%;
            background: linear-gradient(135deg, #8b7cf6 0%, #6c5ce7 100%);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 0.75rem 1.5rem;
            font-weight: 600;
            font-size: 1.02rem;
            letter-spacing: 0.01em;
            box-shadow: 0 4px 18px rgba(139, 124, 246, 0.35);
            transition: transform 0.15s ease, box-shadow 0.15s ease;
        }
        .stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 6px 24px rgba(139, 124, 246, 0.5);
            border: none;
            color: white;
        }
        .stButton > button:active { transform: translateY(0px); }

        /* ---------- Misc ---------- */
        hr {
            border: none;
            border-top: 1px solid rgba(255,255,255,0.08);
            margin: 2rem 0;
        }
        .footer-note {
            text-align: center;
            color: #55556b;
            font-size: 0.82rem;
            margin-top: 2.5rem;
        }
        div[data-testid="stExpander"] {
            background: rgba(0,0,0,0.2);
            border: 1px solid rgba(255,255,255,0.07);
            border-radius: 10px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ------------------------------------------------------------------
# Session state
# ------------------------------------------------------------------
if "results" not in st.session_state:
    st.session_state.results = None
if "last_query" not in st.session_state:
    st.session_state.last_query = ""


# ------------------------------------------------------------------
# Hero section (single self-contained HTML block — safe since nothing
# interactive lives inside it)
# ------------------------------------------------------------------
st.markdown(
    """
    <div class="hero-wrap">
        <div class="hero-badge">✦ Parallel AI Workflow</div>
        <h1 class="hero-title">BuildMate AI</h1>
        <div class="hero-tagline">Learn. Build. Share.</div>
        <p class="hero-desc">
            Turn what you learn into your next project, a polished GitHub README,
            and a LinkedIn post — powered by a parallel AI workflow.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ------------------------------------------------------------------
# Input section
# NOTE: this section contains real interactive widgets (text_area, button),
# so it CANNOT be a single st.markdown HTML string. Instead we use a real
# st.container(border=True) and restyle Streamlit's own border wrapper via
# CSS above — this avoids the "open a <div>, close it later" pattern that
# rendered as empty floating boxes, since every widget here is a genuine
# child of the same Streamlit container.
# ------------------------------------------------------------------
with st.container(border=True):
    st.markdown(
        """
        <div class="section-header">
            <h3 class="section-title"><span class="section-icon">✍️</span> Describe your learning journey</h3>
        </div>
        <p class="section-subtitle">What you learned, what you built, and the technologies involved.</p>
        """,
        unsafe_allow_html=True,
    )

    query = st.text_area(
        label="Your input",
        placeholder=(
            "e.g. Today I learned about REST APIs in FastAPI. I built a small "
            "app that lets users create and fetch to-do items using SQLite as "
            "the database. This helped me understand routing, request "
            "validation with Pydantic, and how to structure a backend project."
        ),
        height=180,
        label_visibility="collapsed",
    )

    generate_clicked = st.button("Generate", type="primary", use_container_width=True)


# ------------------------------------------------------------------
# Generation logic
# ------------------------------------------------------------------
if generate_clicked:
    if not query or not query.strip():
        st.warning("Please describe what you learned or built before generating.")
    else:
        with st.spinner("Running the parallel AI workflow — generating ideas, README, and post..."):
            try:
                info = run_workflow(query.strip())
                st.session_state.results = info
                st.session_state.last_query = query.strip()
            except Exception as e:
                st.session_state.results = None
                st.error(f"Something went wrong while generating your results: {e}")


# ------------------------------------------------------------------
# Output sections
# Each card is rendered as ONE single st.markdown(..., unsafe_allow_html=True)
# call, with the generated Markdown pre-converted to HTML and embedded
# directly inside the same string. This guarantees the card's div actually
# wraps its content in the DOM, instead of the open/close-div pattern that
# previously produced empty floating boxes.
# ------------------------------------------------------------------
if st.session_state.results:
    info = st.session_state.results

    def render_card(icon: str, title: str, subtitle: str, content_md: str):
        content_html = md_to_html(content_md)
        st.markdown(
            f"""
            <div class="glass-card">
                <div class="section-header">
                    <h3 class="section-title"><span class="section-icon">{icon}</span> {htmllib.escape(title)}</h3>
                </div>
                <p class="section-subtitle">{htmllib.escape(subtitle)}</p>
                <div class="output-box">{content_html}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # --- Section 1: Project Ideas ---
    if info.get("advice"):
        render_card(
            "💡", "Project Ideas", "Turn your learning into your next build.",
            info["advice"],
        )

    # --- Section 2: GitHub README ---
    if info.get("repo"):
        render_card(
            "📄", "GitHub README", "Your project, documented and ready to publish.",
            info["repo"],
        )
        with st.expander("Copy raw Markdown"):
            st.code(info["repo"], language="markdown")

    # --- Section 3: LinkedIn Post ---
    if info.get("linkedin_post"):
        render_card(
            "💼", "LinkedIn Post", "Share your learning journey with your network.",
            info["linkedin_post"],
        )
        with st.expander("Copy raw text"):
            st.code(info["linkedin_post"], language=None)

    st.markdown(
        '<div class="footer-note">Generated by BuildMate AI — a parallel LangGraph workflow.</div>',
        unsafe_allow_html=True,
    )