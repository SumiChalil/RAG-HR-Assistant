import streamlit as st
import html as html_lib
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv
load_dotenv(ROOT / ".env")

from main import RAGService

# ── Constants ─────────────────────────────────────────────────────────────────
GRADIENT = "linear-gradient(135deg, #00E676 0%, #8A5CF6 55%, #FF2D95 100%)"
GREEN    = "#00E676"
PURPLE   = "#8A5CF6"
PINK     = "#FF2D95"

SUGGESTIONS = [
    "What is the leave policy?",
    "How do I apply for remote work?",
    "What are the working hours?",
    "How do I request a salary review?",
    "What are the health benefits?",
]

# ── Page config (must be first Streamlit call) ────────────────────────────────
st.set_page_config(
    page_title="HR Assistant",
    page_icon="💼",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
/* ── Base ── */
html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="block-container"] {{
    background-color: #FFFFFF !important;
}}
#MainMenu, footer {{ visibility: hidden; }}
[data-testid="stToolbar"] {{ display: none !important; }}

/* ── Sidebar ── */
[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, #001a0d 0%, #0a001f 50%, #1f0010 100%) !important;
    border-right: 1px solid rgba(255,255,255,0.08) !important;
}}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] div {{
    color: rgba(255,255,255,0.88) !important;
}}
[data-testid="stSidebar"] .stButton > button {{
    background: transparent !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    border-radius: 20px !important;
    color: rgba(255,255,255,0.85) !important;
    font-size: 13px !important;
    padding: 7px 14px !important;
    width: 100% !important;
    text-align: left !important;
    transition: all 0.2s ease !important;
    margin-bottom: 4px !important;
}}
[data-testid="stSidebar"] .stButton > button:hover {{
    background: {GRADIENT} !important;
    border-color: transparent !important;
    color: white !important;
    transform: translateX(3px);
}}
.sidebar-clear-btn > button {{
    background: rgba(255,45,149,0.15) !important;
    border: 1px solid rgba(255,45,149,0.35) !important;
    color: #FF7EC7 !important;
    border-radius: 20px !important;
    font-size: 13px !important;
    width: 100% !important;
    padding: 7px 14px !important;
    transition: all 0.2s ease !important;
}}
.sidebar-clear-btn > button:hover {{
    background: rgba(255,45,149,0.3) !important;
}}

/* ── Chat input ── */
[data-testid="stChatInput"] textarea {{
    border-radius: 28px !important;
    border: 2px solid #EBEBEB !important;
    padding: 13px 22px !important;
    font-size: 14.5px !important;
    background: #FAFAFA !important;
    color: #1a1a1a !important;
    resize: none !important;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06) !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}}
[data-testid="stChatInput"] textarea:focus {{
    border-color: {PURPLE} !important;
    box-shadow: 0 0 0 3px rgba(138,92,246,0.12) !important;
    background: #FFFFFF !important;
}}
[data-testid="stChatInputSubmitButton"] {{
    background: {GRADIENT} !important;
    border-radius: 50% !important;
}}
[data-testid="stChatInputSubmitButton"] svg {{
    fill: white !important;
}}

/* ── WA message rows ── */
.wa-row {{
    display: flex;
    align-items: flex-end;
    margin: 3px 12px;
    gap: 7px;
}}
.wa-row.user {{ justify-content: flex-end; }}
.wa-row.bot  {{ justify-content: flex-start; }}

/* ── Avatars ── */
.wa-avatar {{
    width: 34px;
    height: 34px;
    border-radius: 50%;
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 17px;
    background: {GRADIENT};
    box-shadow: 0 2px 8px rgba(138,92,246,0.35);
}}
.wa-avatar-user {{
    width: 34px;
    height: 34px;
    border-radius: 50%;
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 17px;
    background: linear-gradient(135deg, #00E676, #00B856);
    box-shadow: 0 2px 8px rgba(0,230,118,0.35);
}}

/* ── Bubble ── */
.wa-bubble {{
    max-width: 68%;
    padding: 9px 14px 6px;
    border-radius: 18px;
    font-size: 14.5px;
    line-height: 1.6;
    word-wrap: break-word;
    word-break: break-word;
    box-shadow: 0 1px 5px rgba(0,0,0,0.09);
    position: relative;
}}
.wa-bubble.user {{
    background: {GRADIENT};
    color: #fff;
    border-bottom-right-radius: 4px;
}}
.wa-bubble.bot {{
    background: #F4F4F4;
    color: #1a1a1a;
    border-bottom-left-radius: 4px;
    border: 1px solid #ECECEC;
}}

/* ── Tails ── */
.wa-tail-user {{
    width: 0; height: 0;
    border-left: 7px solid {PINK};
    border-top: 7px solid transparent;
    align-self: flex-end;
    margin-bottom: 4px;
    flex-shrink: 0;
}}
.wa-tail-bot {{
    width: 0; height: 0;
    border-right: 7px solid #F4F4F4;
    border-top: 7px solid transparent;
    align-self: flex-end;
    margin-bottom: 4px;
    flex-shrink: 0;
}}

/* ── Sender label ── */
.wa-sender {{
    font-size: 11.5px;
    font-weight: 700;
    background: {GRADIENT};
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 4px 0 2px 49px;
}}

/* ── Timestamp ── */
.wa-time {{
    font-size: 10.5px;
    margin-top: 3px;
    display: block;
    text-align: right;
    white-space: nowrap;
}}
.wa-bubble.user .wa-time {{ color: rgba(255,255,255,0.65); }}
.wa-bubble.bot  .wa-time {{ color: rgba(0,0,0,0.35); }}
.wa-tick {{ font-size: 11px; color: rgba(255,255,255,0.7); margin-left: 2px; }}

/* ── Date divider ── */
.wa-date-divider {{
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 16px 16px 10px;
    color: #bbb;
    font-size: 11.5px;
}}
.wa-date-divider::before,
.wa-date-divider::after {{
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, transparent, #e0e0e0, transparent);
}}
.wa-date-divider span {{
    background: #F0F0F0;
    padding: 3px 11px;
    border-radius: 10px;
    font-weight: 500;
    white-space: nowrap;
}}

/* ── Empty state ── */
.wa-empty {{
    text-align: center;
    padding: 70px 30px 40px;
}}
.wa-empty-icon {{ font-size: 68px; margin-bottom: 16px; display: block; }}
.wa-empty h3 {{
    background: {GRADIENT};
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-size: 22px;
    margin: 0 0 10px;
}}
.wa-empty p {{ color: #aaa; font-size: 14px; line-height: 1.7; margin: 0; }}

/* ── Typing indicator ── */
.wa-typing-row {{
    display: flex;
    align-items: flex-end;
    gap: 7px;
    margin: 3px 12px;
}}
.wa-typing-bubble {{
    background: #F4F4F4;
    border: 1px solid #ECECEC;
    border-radius: 18px;
    border-bottom-left-radius: 4px;
    padding: 11px 16px 11px;
    display: flex;
    gap: 5px;
    align-items: center;
    box-shadow: 0 1px 5px rgba(0,0,0,0.07);
}}
.wa-typing-bubble span {{
    width: 8px; height: 8px;
    border-radius: 50%;
    animation: wa-bounce 1.3s ease-in-out infinite;
}}
.wa-typing-bubble span:nth-child(1) {{ background: {GREEN};  animation-delay: 0s; }}
.wa-typing-bubble span:nth-child(2) {{ background: {PURPLE}; animation-delay: 0.22s; }}
.wa-typing-bubble span:nth-child(3) {{ background: {PINK};   animation-delay: 0.44s; }}
@keyframes wa-bounce {{
    0%, 60%, 100% {{ transform: translateY(0);   opacity: 0.45; }}
    30%            {{ transform: translateY(-7px); opacity: 1; }}
}}
</style>
""", unsafe_allow_html=True)


# ── Helpers ───────────────────────────────────────────────────────────────────

def now_str() -> str:
    return datetime.now().strftime("%I:%M %p").lstrip("0")


def safe_html(text: str) -> str:
    return html_lib.escape(text).replace("\n\n", "<br><br>").replace("\n", "<br>")


def render_header():
    st.markdown(f"""
    <div style="
        background: {GRADIENT};
        padding: 14px 20px;
        border-radius: 0 0 18px 18px;
        display: flex;
        align-items: center;
        gap: 14px;
        box-shadow: 0 6px 28px rgba(138,92,246,0.22);
        margin-bottom: 8px;
    ">
        <div style="
            width: 50px; height: 50px; border-radius: 50%;
            background: rgba(255,255,255,0.18);
            border: 2.5px solid rgba(255,255,255,0.45);
            display: flex; align-items: center;
            justify-content: center; font-size: 24px; flex-shrink: 0;
        ">💼</div>
        <div style="flex: 1; min-width: 0;">
            <div style="font-size: 17px; font-weight: 700; color: #fff; letter-spacing: 0.2px;">
                HR Assistant
            </div>
            <div style="font-size: 12px; color: rgba(255,255,255,0.82); margin-top: 2px; display:flex; align-items:center; gap:5px;">
                <span style="
                    display: inline-block; width: 7px; height: 7px;
                    background: #AFFFCE; border-radius: 50%;
                    box-shadow: 0 0 6px {GREEN};
                "></span>
                Online &nbsp;·&nbsp; Employee Handbook AI
            </div>
        </div>
        <div style="text-align: right; flex-shrink: 0;">
            <div style="font-size: 10px; color: rgba(255,255,255,0.65);">Powered by</div>
            <div style="font-size: 12px; font-weight: 600; color: #fff;">GPT-3.5 · RAG</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_date_divider(label: str):
    st.markdown(f"""
    <div class="wa-date-divider"><span>{label}</span></div>
    """, unsafe_allow_html=True)


def render_user_bubble(content: str, time: str):
    st.markdown(f"""
    <div class="wa-row user">
        <div class="wa-bubble user">
            {safe_html(content)}
            <span class="wa-time">{time}<span class="wa-tick"> ✓✓</span></span>
        </div>
        <div class="wa-tail-user"></div>
        <div class="wa-avatar-user">👤</div>
    </div>
    """, unsafe_allow_html=True)


def render_bot_bubble(content: str, time: str, show_label: bool = True):
    label = '<div class="wa-sender">HR Assistant</div>' if show_label else ""
    st.markdown(f"""
    {label}
    <div class="wa-row bot">
        <div class="wa-avatar">🤖</div>
        <div class="wa-tail-bot"></div>
        <div class="wa-bubble bot">
            {safe_html(content)}
            <span class="wa-time">{time}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_typing():
    return st.markdown(f"""
    <div class="wa-sender">HR Assistant</div>
    <div class="wa-typing-row">
        <div class="wa-avatar">🤖</div>
        <div class="wa-tail-bot"></div>
        <div class="wa-typing-bubble">
            <span></span><span></span><span></span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_empty_state():
    st.markdown(f"""
    <div class="wa-empty">
        <span class="wa-empty-icon">💬</span>
        <h3>Ask me anything!</h3>
        <p>
            I'm your AI-powered HR assistant.<br>
            Ask me about leave policies, benefits,<br>
            working hours, or anything in the<br>
            employee handbook.
        </p>
    </div>
    """, unsafe_allow_html=True)


# ── Session state ─────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

if "rag" not in st.session_state:
    st.session_state.rag = None

if "initialized" not in st.session_state:
    st.session_state.initialized = False


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style="text-align: center; padding: 24px 0 16px;">
        <div style="
            width: 72px; height: 72px; border-radius: 50%;
            background: {GRADIENT};
            display: flex; align-items: center; justify-content: center;
            font-size: 36px; margin: 0 auto 14px;
            box-shadow: 0 4px 20px rgba(138,92,246,0.45);
        ">💼</div>
        <div style="font-size: 18px; font-weight: 700; color: #fff; margin-bottom: 4px;">
            HR Assistant
        </div>
        <div style="font-size: 12px; color: rgba(255,255,255,0.55);">
            Employee Handbook AI
        </div>
    </div>
    <div style="height: 1px; background: rgba(255,255,255,0.1); margin: 0 0 18px;"></div>
    <div style="font-size: 12px; font-weight: 600; color: rgba(255,255,255,0.5);
                text-transform: uppercase; letter-spacing: 1px; margin-bottom: 10px;">
        Quick Questions
    </div>
    """, unsafe_allow_html=True)

    for q in SUGGESTIONS:
        if st.button(q, key=f"sugg_{q}", use_container_width=True):
            st.session_state["pending_query"] = q

    st.markdown("""
    <div style="height: 1px; background: rgba(255,255,255,0.1); margin: 18px 0 16px;"></div>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="sidebar-clear-btn">', unsafe_allow_html=True)
        if st.button("🗑  Clear Chat", use_container_width=True, key="clear_btn"):
            st.session_state.messages = []
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(f"""
    <div style="
        margin-top: 32px;
        text-align: center; font-size: 11px;
        color: rgba(255,255,255,0.3);
        line-height: 1.9;
        padding-bottom: 8px;
    ">
        OpenAI · ChromaDB · LangChain<br>
        Built with Streamlit
    </div>
    """, unsafe_allow_html=True)


# ── Main area ─────────────────────────────────────────────────────────────────
render_header()

# Initialize RAG service once
if not st.session_state.initialized:
    with st.spinner("Loading HR knowledge base..."):
        try:
            st.session_state.rag = RAGService()
            st.session_state.initialized = True
        except Exception as exc:
            st.error(f"Could not initialize HR Assistant: {exc}")
            st.stop()

# Render conversation history
if not st.session_state.messages:
    render_empty_state()
else:
    today = datetime.now().strftime("%B %d, %Y")
    render_date_divider(today)
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            render_user_bubble(msg["content"], msg["time"])
        else:
            render_bot_bubble(msg["content"], msg["time"])

# Resolve prompt from sidebar quick-question or chat input
pending = st.session_state.get("pending_query")
if pending:
    del st.session_state["pending_query"]

typed = st.chat_input("Ask about HR policies, leave, benefits…")
prompt = typed or pending

if prompt:
    user_time = now_str()
    st.session_state.messages.append({"role": "user", "content": prompt, "time": user_time})

    typing_slot = st.empty()
    with typing_slot:
        render_typing()

    try:
        response = st.session_state.rag.ask(prompt)
    except Exception as exc:
        response = f"Sorry, something went wrong: {exc}"

    typing_slot.empty()

    bot_time = now_str()
    st.session_state.messages.append({"role": "bot", "content": response, "time": bot_time})
    st.rerun()
