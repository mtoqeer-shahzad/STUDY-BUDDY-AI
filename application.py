import os
import streamlit as st
from dotenv import load_dotenv
from src.utils.helper import *
from src.generator.question_generator import QuestionGenerator

load_dotenv()

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;600&display=swap');

:root {
    --bg-0:        #020409;
    --bg-glass:    rgba(255,255,255,0.03);
    --bg-glass2:   rgba(255,255,255,0.06);
    --neon-blue:   #00d4ff;
    --neon-green:  #00ff88;
    --neon-pink:   #ff006e;
    --neon-amber:  #ffb300;
    --neon-violet: #9d4edd;
    --groq-orange: #ff6b35;
    --text-bright: #ffffff;
    --text-main:   #e2e8f0;
    --text-dim:    #64748b;
    --border-dim:  rgba(0,212,255,0.08);
    --border-glow: rgba(0,212,255,0.25);

    /* Sidebar — GitHub-style natural dark */
    --sb-bg:      #0d1117;
    --sb-surface: #161b22;
    --sb-border:  rgba(255,255,255,0.07);
    --sb-text:    #c9d1d9;
    --sb-muted:   #8b949e;
}

*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"], .stApp {
    font-family: 'Outfit', sans-serif !important;
    background: var(--bg-0) !important;
    color: var(--text-main) !important;
}
.stApp {
    background:
        radial-gradient(ellipse 80% 50% at 20% -10%, rgba(0,212,255,0.06) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 110%, rgba(157,78,221,0.06) 0%, transparent 60%),
        var(--bg-0) !important;
}
.stApp::before {
    content: '';
    position: fixed; inset: 0;
    background-image:
        linear-gradient(rgba(0,212,255,0.015) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,212,255,0.015) 1px, transparent 1px);
    background-size: 60px 60px;
    pointer-events: none; z-index: 0;
}

/* ══════════════════════════════════
   SIDEBAR — Natural & Clean
══════════════════════════════════ */
section[data-testid="stSidebar"] {
    background: var(--sb-bg) !important;
    border-right: 1px solid var(--sb-border) !important;
}
section[data-testid="stSidebar"] > div {
    padding: 0 !important;
}
section[data-testid="stSidebar"] * {
    font-family: 'Outfit', sans-serif !important;
    color: var(--sb-text) !important;
}

.sb-brand {
    display: flex; align-items: center; gap: 0.65rem;
    padding: 1.1rem 1rem 1rem;
    border-bottom: 1px solid var(--sb-border);
}
.sb-icon {
    width: 32px; height: 32px; border-radius: 8px; flex-shrink: 0;
    background: linear-gradient(135deg, rgba(0,212,255,0.18), rgba(157,78,221,0.18));
    border: 1px solid rgba(0,212,255,0.18);
    display: flex; align-items: center; justify-content: center; font-size: 0.95rem;
}
.sb-title { font-size: 0.88rem; font-weight: 700; color: #e6edf3 !important; line-height: 1.2; }
.sb-sub   { font-size: 0.62rem; color: var(--sb-muted) !important; margin-top: 1px; }

.sb-status {
    display: flex; align-items: center; gap: 0.5rem;
    margin: 0.8rem 0.9rem 0;
    padding: 0.42rem 0.7rem;
    background: rgba(63,185,80,0.05);
    border: 1px solid rgba(63,185,80,0.14);
    border-radius: 7px;
}
.sb-dot {
    width: 6px; height: 6px; border-radius: 50%;
    background: #3fb950; box-shadow: 0 0 5px #3fb950;
    flex-shrink: 0; animation: pulse 2.5s ease infinite;
}
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.35} }
.sb-status-model { font-size: 0.73rem; font-weight: 600; color: var(--sb-text) !important; }
.sb-status-badge {
    margin-left: auto; font-size: 0.59rem; font-weight: 700;
    color: var(--groq-orange) !important;
    background: rgba(255,107,53,0.1); border: 1px solid rgba(255,107,53,0.2);
    padding: 0.1rem 0.42rem; border-radius: 4px; letter-spacing: 0.05em;
}

.sb-section {
    font-size: 0.6rem !important; font-weight: 700 !important;
    letter-spacing: 0.15em !important; text-transform: uppercase !important;
    color: var(--sb-muted) !important;
    padding: 1rem 1rem 0.3rem !important; display: block !important;
}
.sb-divider { height: 1px; background: var(--sb-border); margin: 0.5rem 0.85rem 0.7rem; }

.sb-footer {
    position: absolute; bottom: 0; left: 0; right: 0;
    padding: 0.75rem 1rem;
    border-top: 1px solid var(--sb-border);
    background: rgba(0,0,0,0.15);
    display: flex; align-items: center; justify-content: space-between;
}
.sb-footer-text { font-size: 0.62rem; color: var(--sb-muted) !important; line-height: 1.5; }
.sb-footer-text b { color: var(--sb-text) !important; font-weight: 600; }
.sb-ver {
    font-family: 'JetBrains Mono', monospace; font-size: 0.58rem;
    color: var(--sb-muted) !important;
    background: rgba(255,255,255,0.04); border: 1px solid var(--sb-border);
    padding: 0.17rem 0.42rem; border-radius: 5px;
}

/* Inputs */
section[data-testid="stSidebar"] .stTextInput > div > div > input {
    background: var(--sb-surface) !important;
    border: 1px solid rgba(255,255,255,0.09) !important;
    border-radius: 8px !important;
    color: var(--sb-text) !important;
    font-size: 0.83rem !important;
    padding: 0.46rem 0.7rem !important;
    transition: border-color 0.15s, box-shadow 0.15s !important;
}
section[data-testid="stSidebar"] .stTextInput > div > div > input:focus {
    border-color: rgba(88,166,255,0.4) !important;
    box-shadow: 0 0 0 3px rgba(88,166,255,0.07) !important;
    outline: none !important;
}
section[data-testid="stSidebar"] .stTextInput > div > div > input::placeholder {
    color: var(--sb-muted) !important; font-size: 0.79rem !important;
}
section[data-testid="stSidebar"] .stSelectbox > div > div,
section[data-testid="stSidebar"] .stNumberInput > div > div > input {
    background: var(--sb-surface) !important;
    border: 1px solid rgba(255,255,255,0.09) !important;
    border-radius: 8px !important;
    color: var(--sb-text) !important;
    font-size: 0.83rem !important;
}
section[data-testid="stSidebar"] label {
    font-size: 0.67rem !important; font-weight: 600 !important;
    letter-spacing: 0.06em !important; text-transform: uppercase !important;
    color: var(--sb-muted) !important;
}

/* Primary CTA */
section[data-testid="stSidebar"] .stButton > button {
    width: 100% !important;
    background: linear-gradient(135deg, #1e6fa8, #553899) !important;
    border: none !important; border-radius: 9px !important;
    color: #fff !important; font-weight: 700 !important; font-size: 0.85rem !important;
    padding: 0.56rem 1rem !important; letter-spacing: 0.01em !important;
    transition: all 0.18s !important;
    box-shadow: 0 2px 10px rgba(30,111,168,0.2) !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
    opacity: 0.9 !important; transform: translateY(-1px) !important;
    box-shadow: 0 4px 18px rgba(30,111,168,0.35) !important;
}
section[data-testid="stSidebar"] .stButton > button:active {
    transform: none !important;
}

/* ══════════════════════════════════
   MAIN CONTENT
══════════════════════════════════ */
.top-bar {
    display: flex; align-items: center; justify-content: space-between;
    padding: 1rem 0 0.5rem;
    border-bottom: 1px solid var(--border-dim);
    margin-bottom: 1.5rem;
    animation: fadeSlideDown 0.6s ease both;
}
.top-bar-left { display: flex; align-items: center; gap: 0.75rem; }
.top-logo {
    width: 38px; height: 38px;
    background: linear-gradient(135deg, var(--neon-blue), var(--neon-violet));
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem; box-shadow: 0 0 20px rgba(0,212,255,0.35);
}
.top-app-name { font-size: 1.1rem; font-weight: 800; color: var(--text-bright); letter-spacing: -0.02em; }
.top-app-sub  { font-size: 0.68rem; color: var(--text-dim); margin-top: -2px; }
.top-bar-right { display: flex; align-items: center; gap: 0.5rem; }
.pill {
    display: inline-flex; align-items: center; gap: 0.3rem;
    padding: 0.25rem 0.7rem; border-radius: 999px;
    font-size: 0.68rem; font-weight: 700; letter-spacing: 0.08em;
    text-transform: uppercase; border: 1px solid;
}
.pill-groq { background:rgba(255,107,53,0.1); border-color:rgba(255,107,53,0.35); color:var(--groq-orange); }
.pill-live  { background:rgba(0,255,136,0.08); border-color:rgba(0,255,136,0.3); color:var(--neon-green); }
.pill-live::before {
    content:''; display:inline-block; width:6px; height:6px; border-radius:50%;
    background:var(--neon-green); box-shadow:0 0 8px var(--neon-green);
    animation: blink 1.4s ease-in-out infinite;
}
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.3} }

.hero {
    position: relative; background: var(--bg-glass);
    border: 1px solid var(--border-dim); border-radius: 24px;
    padding: 2.5rem 2.5rem 2rem; margin-bottom: 2rem;
    overflow: hidden; backdrop-filter: blur(20px);
    animation: fadeSlideUp 0.7s ease 0.1s both;
}
.hero::before {
    content:''; position:absolute; top:0; left:0; right:0; height:1px;
    background: linear-gradient(90deg, transparent, var(--neon-blue), transparent);
}
.hero::after {
    content:''; position:absolute; top:-100px; right:-100px;
    width:400px; height:400px;
    background: radial-gradient(circle, rgba(0,212,255,0.05) 0%, transparent 60%);
    pointer-events:none;
}
.hero-kicker {
    font-size:0.65rem; font-weight:700; letter-spacing:0.3em;
    text-transform:uppercase; color:var(--neon-blue);
    margin-bottom:0.8rem; display:flex; align-items:center; gap:0.6rem;
}
.kicker-line { display:inline-block; width:24px; height:1px; background:linear-gradient(90deg,var(--neon-blue),transparent); }
.hero-h1 {
    font-size: clamp(1.8rem, 4vw, 3rem); font-weight: 900;
    line-height: 1.1; letter-spacing: -0.04em; color: var(--text-bright); margin: 0 0 0.2rem;
}
.hero-h1 .hl {
    background: linear-gradient(135deg, var(--neon-blue) 0%, var(--neon-violet) 50%, var(--neon-blue) 100%);
    background-size: 200% auto;
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
    animation: shimmer 4s linear infinite;
}
@keyframes shimmer { 0%{background-position:0% center} 100%{background-position:200% center} }
.hero-desc { font-size:0.92rem; color:var(--text-dim); max-width:480px; line-height:1.7; margin:0.8rem 0 1.4rem; }
.hero-tags { display:flex; flex-wrap:wrap; gap:0.5rem; }
.htag { padding:0.3rem 0.85rem; border-radius:999px; font-size:0.72rem; font-weight:600; border:1px solid; }
.htag-b { background:rgba(0,212,255,0.08);  border-color:rgba(0,212,255,0.25);  color:#7dd3fc; }
.htag-g { background:rgba(0,255,136,0.08);  border-color:rgba(0,255,136,0.25);  color:#6ee7b7; }
.htag-v { background:rgba(157,78,221,0.1);  border-color:rgba(157,78,221,0.3);  color:#c4b5fd; }
.htag-o { background:rgba(255,107,53,0.1);  border-color:rgba(255,107,53,0.3);  color:#fdba74; }

.metrics-row {
    display: grid; grid-template-columns: repeat(4,1fr);
    gap: 0.75rem; margin-bottom: 2rem;
    animation: fadeSlideUp 0.7s ease 0.2s both;
}
.metric-card {
    background: var(--bg-glass); border: 1px solid var(--border-dim);
    border-radius: 16px; padding: 1.1rem 1rem; position: relative;
    overflow: hidden; transition: border-color 0.3s, transform 0.2s;
    backdrop-filter: blur(10px);
}
.metric-card::before {
    content:''; position:absolute; top:0; left:0; right:0;
    height:2px; opacity:0; transition:opacity 0.3s;
}
.metric-card:hover { border-color: var(--border-glow); transform: translateY(-2px); }
.metric-card:hover::before { opacity: 1; }
.mc-blue::before  { background:linear-gradient(90deg,var(--neon-blue),transparent); }
.mc-green::before { background:linear-gradient(90deg,var(--neon-green),transparent); }
.mc-pink::before  { background:linear-gradient(90deg,var(--neon-pink),transparent); }
.mc-amber::before { background:linear-gradient(90deg,var(--neon-amber),transparent); }
.metric-icon { font-size:1.2rem; margin-bottom:0.5rem; }
.metric-value { font-family:'JetBrains Mono',monospace; font-size:1.6rem; font-weight:600; line-height:1; margin-bottom:0.25rem; }
.mv-blue{color:var(--neon-blue);} .mv-green{color:var(--neon-green);}
.mv-pink{color:var(--neon-pink);} .mv-amber{color:var(--neon-amber);}
.metric-label { font-size:0.68rem; font-weight:600; text-transform:uppercase; letter-spacing:0.12em; color:var(--text-dim); }

.sec-div { display:flex; align-items:center; gap:0.8rem; margin:2rem 0 1.2rem; }
.sec-icon { width:32px; height:32px; border-radius:8px; display:flex; align-items:center; justify-content:center; font-size:0.9rem; flex-shrink:0; }
.si-b{background:rgba(0,212,255,0.1); border:1px solid rgba(0,212,255,0.2);}
.si-g{background:rgba(0,255,136,0.1); border:1px solid rgba(0,255,136,0.2);}
.si-a{background:rgba(255,179,0,0.1); border:1px solid rgba(255,179,0,0.2);}
.sec-title { font-size:1rem; font-weight:700; color:var(--text-bright); }
.sec-line { flex:1; height:1px; background:linear-gradient(90deg,var(--border-dim),transparent); }

.score-wrap {
    background:var(--bg-glass); border:1px solid var(--border-glow);
    border-radius:24px; padding:2.5rem; text-align:center;
    position:relative; overflow:hidden;
    box-shadow:0 0 40px rgba(0,212,255,0.1); margin-bottom:1.5rem;
}
.score-wrap::before {
    content:''; position:absolute; top:0; left:0; right:0; height:1px;
    background: linear-gradient(90deg,transparent,var(--neon-blue),var(--neon-violet),transparent);
}
.score-num {
    font-family:'JetBrains Mono',monospace; font-size:5rem; font-weight:600; line-height:1;
    background:linear-gradient(135deg,var(--neon-blue),var(--neon-violet));
    -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;
    filter:drop-shadow(0 0 20px rgba(0,212,255,0.35));
}
.score-pct { font-size:2rem; vertical-align:super; background:linear-gradient(135deg,var(--neon-blue),var(--neon-violet)); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; }
.score-caption { font-size:0.72rem; font-weight:700; letter-spacing:0.2em; text-transform:uppercase; color:var(--text-dim); margin-top:0.4rem; }
.score-grade { display:inline-flex; align-items:center; gap:0.4rem; margin-top:1rem; padding:0.4rem 1.2rem; border-radius:999px; font-size:0.82rem; font-weight:700; }
.sg-e{background:rgba(0,255,136,0.1); border:1px solid rgba(0,255,136,0.3); color:var(--neon-green);}
.sg-g{background:rgba(0,212,255,0.1); border:1px solid rgba(0,212,255,0.3); color:var(--neon-blue);}
.sg-a{background:rgba(255,179,0,0.1); border:1px solid rgba(255,179,0,0.3); color:var(--neon-amber);}
.sg-p{background:rgba(255,0,110,0.1); border:1px solid rgba(255,0,110,0.3); color:var(--neon-pink);}
.prog-wrap { background:rgba(255,255,255,0.04); border-radius:999px; height:6px; margin-top:1.2rem; overflow:hidden; }
.prog-fill { height:100%; border-radius:999px; background:linear-gradient(90deg,var(--neon-blue),var(--neon-violet)); box-shadow:0 0 12px rgba(0,212,255,0.5); }

.res-card { border-radius:16px; padding:1.1rem 1.3rem; margin-bottom:0.75rem; position:relative; overflow:hidden; }
.res-ok  { background:linear-gradient(135deg,rgba(0,255,136,0.04),rgba(0,212,255,0.02)); border:1px solid rgba(0,255,136,0.15); }
.res-bad { background:linear-gradient(135deg,rgba(255,0,110,0.05),rgba(255,107,53,0.02)); border:1px solid rgba(255,0,110,0.15); }
.res-ok::before  { content:''; position:absolute; left:0; top:0; bottom:0; width:3px; background:linear-gradient(180deg,var(--neon-green),var(--neon-blue)); border-radius:3px 0 0 3px; }
.res-bad::before { content:''; position:absolute; left:0; top:0; bottom:0; width:3px; background:linear-gradient(180deg,var(--neon-pink),var(--groq-orange)); border-radius:3px 0 0 3px; }
.res-status { font-size:0.65rem; font-weight:700; letter-spacing:0.15em; text-transform:uppercase; margin-bottom:0.4rem; }
.ss-ok{color:var(--neon-green);} .ss-bad{color:var(--neon-pink);}
.res-q  { font-size:0.92rem; font-weight:500; color:var(--text-main); margin-bottom:0.6rem; padding-left:0.5rem; line-height:1.5; }
.res-ans { display:flex; gap:1rem; flex-wrap:wrap; padding-left:0.5rem; }
.ans-chip { font-size:0.78rem; padding:0.2rem 0.7rem; border-radius:6px; font-family:'JetBrains Mono',monospace; }
.ac-wrong{background:rgba(255,0,110,0.1); color:#fda4af; border:1px solid rgba(255,0,110,0.2);}
.ac-right{background:rgba(0,255,136,0.1); color:#6ee7b7; border:1px solid rgba(0,255,136,0.2);}
.ac-ans  {background:rgba(0,212,255,0.1); color:#7dd3fc; border:1px solid rgba(0,212,255,0.2);}

.empty-state { text-align:center; padding:5rem 2rem; border:1px dashed rgba(0,212,255,0.1); border-radius:24px; background:var(--bg-glass); backdrop-filter:blur(10px); }
.empty-icon { font-size:3.5rem; margin-bottom:1rem; filter:drop-shadow(0 0 20px rgba(0,212,255,0.3)); animation:float 3s ease-in-out infinite; }
@keyframes float { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-10px)} }
.empty-title { font-size:1.4rem; font-weight:800; color:var(--text-bright); margin-bottom:0.6rem; letter-spacing:-0.02em; }
.empty-sub   { font-size:0.88rem; color:var(--text-dim); line-height:1.7; max-width:360px; margin:0 auto 1.5rem; }
.empty-steps { display:inline-flex; gap:0.4rem; align-items:center; font-size:0.75rem; color:var(--text-dim); background:var(--bg-glass2); padding:0.5rem 1rem; border-radius:10px; border:1px solid var(--border-dim); }
.step-n { width:18px; height:18px; border-radius:50%; background:rgba(0,212,255,0.12); border:1px solid rgba(0,212,255,0.25); display:inline-flex; align-items:center; justify-content:center; font-size:0.6rem; font-weight:700; color:var(--neon-blue); }

.stButton>button {
    background:linear-gradient(135deg,rgba(0,212,255,0.1),rgba(157,78,221,0.1)) !important;
    border:1px solid rgba(0,212,255,0.2) !important; border-radius:12px !important;
    color:var(--neon-blue) !important; font-family:'Outfit',sans-serif !important;
    font-weight:700 !important; font-size:0.88rem !important; padding:0.65rem 1.5rem !important;
    transition:all 0.2s !important;
}
.stButton>button:hover {
    background:linear-gradient(135deg,rgba(0,212,255,0.2),rgba(157,78,221,0.2)) !important;
    border-color:var(--neon-blue) !important; box-shadow:0 0 18px rgba(0,212,255,0.18) !important;
    transform:translateY(-1px) !important; color:white !important;
}
.stDownloadButton>button {
    background:linear-gradient(135deg,rgba(0,255,136,0.1),rgba(0,212,255,0.06)) !important;
    border-color:rgba(0,255,136,0.25) !important; color:var(--neon-green) !important;
}
.stSuccess{background:rgba(0,255,136,0.05) !important; border:1px solid rgba(0,255,136,0.18) !important; border-radius:10px !important; color:#6ee7b7 !important;}
.stError  {background:rgba(255,0,110,0.05)  !important; border:1px solid rgba(255,0,110,0.18)  !important; border-radius:10px !important; color:#fda4af !important;}
.stWarning{background:rgba(255,179,0,0.05)  !important; border:1px solid rgba(255,179,0,0.18)  !important; border-radius:10px !important;}
div[data-testid="stMarkdownContainer"] hr { border:none !important; border-top:1px solid var(--border-dim) !important; }

@keyframes fadeSlideUp   { from{opacity:0;transform:translateY(16px)} to{opacity:1;transform:translateY(0)} }
@keyframes fadeSlideDown { from{opacity:0;transform:translateY(-10px)} to{opacity:1;transform:translateY(0)} }

#MainMenu,footer,header{visibility:hidden;} .stDeployButton{display:none;}
div.block-container{padding-top:1.5rem !important; max-width:900px !important;}
::-webkit-scrollbar{width:4px;} ::-webkit-scrollbar-track{background:var(--bg-0);}
::-webkit-scrollbar-thumb{background:rgba(0,212,255,0.15);border-radius:4px;}
</style>
"""


def get_grade(pct):
    if pct >= 80: return "sg-e", "🏆 Excellent"
    if pct >= 60: return "sg-g", "✨ Good Job"
    if pct >= 40: return "sg-a", "📚 Keep Going"
    return "sg-p", "💪 Don't Give Up"


def render_top_bar(topic):
    t = topic if topic else "Study Buddy AI"
    st.markdown(f"""
    <div class="top-bar">
        <div class="top-bar-left">
            <div class="top-logo">🎯</div>
            <div>
                <div class="top-app-name">{t}</div>
                <div class="top-app-sub">AI-powered learning assistant</div>
            </div>
        </div>
        <div class="top-bar-right">
            <span class="pill pill-groq">⚡ Groq</span>
            <span class="pill pill-live">Live</span>
        </div>
    </div>""", unsafe_allow_html=True)


def render_hero(topic, qtype, difficulty, num_q):
    icons = {"Multiple Choice": "🔵", "Fill in the Blank": "✏️"}
    icon  = icons.get(qtype, "📖")
    diff_cls = {"Easy":"htag-g","Medium":"htag-b","Hard":"htag-v"}.get(difficulty,"htag-b")
    td = topic if topic else "Your Next Challenge"
    st.markdown(f"""
    <div class="hero">
        <div class="hero-kicker"><span class="kicker-line"></span>AI Quiz Generator · Groq × LLaMA 3.3</div>
        <h1 class="hero-h1">{icon} <span class="hl">{td}</span></h1>
        <p class="hero-desc">Sharpen your skills with LLaMA&nbsp;3.3 powered questions.<br>Every quiz is unique — generated live via Groq's ultra-fast inference.</p>
        <div class="hero-tags">
            <span class="htag htag-b">📝 {qtype}</span>
            <span class="htag {diff_cls}">📊 {difficulty}</span>
            <span class="htag htag-o">❓ {num_q} Questions</span>
            <span class="htag htag-v">🤖 LLaMA 3.3 70B</span>
        </div>
    </div>""", unsafe_allow_html=True)


def render_metrics(total, correct=None, submitted=False):
    if submitted and correct is not None:
        wrong = total - correct
        pct   = round((correct / total) * 100) if total else 0
        st.markdown(f"""
        <div class="metrics-row">
            <div class="metric-card mc-blue"><div class="metric-icon">📋</div><div class="metric-value mv-blue">{total}</div><div class="metric-label">Total</div></div>
            <div class="metric-card mc-green"><div class="metric-icon">✅</div><div class="metric-value mv-green">{correct}</div><div class="metric-label">Correct</div></div>
            <div class="metric-card mc-pink"><div class="metric-icon">❌</div><div class="metric-value mv-pink">{wrong}</div><div class="metric-label">Wrong</div></div>
            <div class="metric-card mc-amber"><div class="metric-icon">🎯</div><div class="metric-value mv-amber">{pct}%</div><div class="metric-label">Score</div></div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="metrics-row">
            <div class="metric-card mc-blue"><div class="metric-icon">❓</div><div class="metric-value mv-blue">{total}</div><div class="metric-label">Questions</div></div>
            <div class="metric-card mc-green"><div class="metric-icon">⚡</div><div class="metric-value mv-green">Groq</div><div class="metric-label">Engine</div></div>
            <div class="metric-card mc-amber"><div class="metric-icon">🤖</div><div class="metric-value" style="color:var(--neon-violet)">3.3</div><div class="metric-label">LLaMA</div></div>
            <div class="metric-card mc-amber"><div class="metric-icon">📊</div><div class="metric-value mv-amber">Live</div><div class="metric-label">Generated</div></div>
        </div>""", unsafe_allow_html=True)


def sec_divider(icon, title, cls="si-b"):
    st.markdown(f"""
    <div class="sec-div">
        <div class="sec-icon {cls}">{icon}</div>
        <span class="sec-title">{title}</span>
        <div class="sec-line"></div>
    </div>""", unsafe_allow_html=True)


def render_score(pct, correct, total):
    gc, gl = get_grade(pct)
    st.markdown(f"""
    <div class="score-wrap">
        <div class="score-num">{pct}<span class="score-pct">%</span></div>
        <div class="score-caption">Final Score — {correct} of {total} correct</div>
        <div class="score-grade {gc}">{gl}</div>
        <div class="prog-wrap"><div class="prog-fill" style="width:{pct}%"></div></div>
    </div>""", unsafe_allow_html=True)


def render_res_card(num, q, correct, user_ans, correct_ans):
    if correct:
        st.markdown(f"""
        <div class="res-card res-ok">
            <div class="res-status ss-ok">✅ Question {num} — Correct</div>
            <div class="res-q">{q}</div>
            <div class="res-ans"><span class="ans-chip ac-right">Your answer: {user_ans}</span></div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="res-card res-bad">
            <div class="res-status ss-bad">❌ Question {num} — Wrong</div>
            <div class="res-q">{q}</div>
            <div class="res-ans">
                <span class="ans-chip ac-wrong">You: {user_ans}</span>
                <span class="ans-chip ac-ans">✓ Correct: {correct_ans}</span>
            </div>
        </div>""", unsafe_allow_html=True)


def main():
    st.set_page_config(
        page_title="Study Buddy AI — Groq Edition",
        page_icon="🎯",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

    for k, v in {
        "quiz_manager":   None,
        "quiz_generated": False,
        "quiz_submitted": False,
        "c_topic": "", "c_type": "Multiple Choice",
        "c_diff":  "Medium", "c_num": 5,
    }.items():
        if k not in st.session_state:
            st.session_state[k] = v

    if st.session_state.quiz_manager is None:
        st.session_state.quiz_manager = QuizManager()

    # ── SIDEBAR ──────────────────────────────────────────
    with st.sidebar:

        st.markdown("""
        <div class="sb-brand">
            <div class="sb-icon">🎯</div>
            <div>
                <div class="sb-title">Study Buddy AI</div>
                <div class="sb-sub">Groq Edition · v2.0</div>
            </div>
        </div>""", unsafe_allow_html=True)

        st.markdown("""
        <div class="sb-status">
            <div class="sb-dot"></div>
            <span class="sb-status-model">LLaMA 3.3 70B</span>
            <span class="sb-status-badge">GROQ</span>
        </div>""", unsafe_allow_html=True)

        st.markdown('<span class="sb-section">Quiz Settings</span>', unsafe_allow_html=True)

        topic = st.text_input(
            "Topic",
            placeholder="e.g. Machine Learning, Python, WW2...",
            value=st.session_state.c_topic,
        )
        question_type = st.selectbox("Question Type", ["Multiple Choice", "Fill in the Blank"])
        difficulty    = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"], index=1)
        num_questions = st.number_input("Number of Questions", min_value=1, max_value=10, value=5)

        st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)

        if st.button("⚡  Generate Quiz", use_container_width=True):
            if not topic.strip():
                st.error("⚠️ Please enter a topic first!")
            else:
                st.session_state.update({
                    "quiz_submitted": False, "quiz_generated": False,
                    "c_topic": topic, "c_type": question_type,
                    "c_diff":  difficulty, "c_num": num_questions,
                    "quiz_manager": QuizManager()
                })
                with st.spinner("Generating your quiz..."):
                    gen = QuestionGenerator()
                    ok  = st.session_state.quiz_manager.generate_questions(
                        gen, topic, question_type, difficulty, num_questions
                    )
                st.session_state.quiz_generated = ok
                if ok: st.success("Quiz is ready!")
                else:  st.error("Generation failed. Please try again.")
                st.rerun()

        if st.session_state.quiz_generated and not st.session_state.quiz_submitted:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("↩  New Topic", use_container_width=True):
                st.session_state.update({
                    "quiz_generated": False, "quiz_submitted": False,
                    "quiz_manager":   QuizManager()
                })
                st.rerun()

        st.markdown("""
        <div class="sb-footer">
            <div class="sb-footer-text">Powered by <b>Groq</b><br>via LangChain</div>
            <span class="sb-ver">v2.0</span>
        </div>""", unsafe_allow_html=True)

    # ── MAIN ─────────────────────────────────────────────
    t  = st.session_state.c_topic
    qt = st.session_state.c_type
    d  = st.session_state.c_diff
    n  = st.session_state.c_num

    render_top_bar(t)
    render_hero(t, qt, d, n)

    if not st.session_state.quiz_generated:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-icon">🧠</div>
            <div class="empty-title">Ready to Challenge Yourself?</div>
            <div class="empty-sub">
                Enter any topic in the sidebar and let Groq's
                LLaMA 3.3 build a custom quiz in seconds.
            </div>
            <div class="empty-steps">
                <span class="step-n">1</span>&nbsp;Enter topic&nbsp;&nbsp;
                <span class="step-n">2</span>&nbsp;Set difficulty&nbsp;&nbsp;
                <span class="step-n">3</span>&nbsp;Hit Generate
            </div>
        </div>""", unsafe_allow_html=True)
        return

    mgr = st.session_state.quiz_manager

    if st.session_state.quiz_generated and mgr.questions and not st.session_state.quiz_submitted:
        render_metrics(len(mgr.questions))
        sec_divider("📝", "Answer All Questions", "si-b")
        mgr.attempt_quiz()
        st.markdown("<br>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            if st.button("✅  Submit & See Results", use_container_width=True):
                mgr.evaluate_quiz()
                st.session_state.quiz_submitted = True
                st.rerun()

    if st.session_state.quiz_submitted:
        df = mgr.generate_result_dataframe()
        if not df.empty:
            correct = int(df["is_correct"].sum())
            total   = len(df)
            pct     = round((correct / total) * 100)

            render_metrics(total, correct, submitted=True)
            render_score(pct, correct, total)

            sec_divider("📊", "Detailed Breakdown", "si-g")
            for _, row in df.iterrows():
                render_res_card(
                    row['question_number'], row['question'],
                    row['is_correct'], row['user_answer'], row['correct_answer']
                )

            st.markdown("<br>", unsafe_allow_html=True)
            sec_divider("💾", "Export & Actions", "si-a")
            c1, c2, c3 = st.columns(3)
            with c1:
                saved = mgr.save_to_csv()
                if saved:
                    with open(saved, 'rb') as f:
                        st.download_button(
                            "⬇️ Download CSV", f.read(),
                            os.path.basename(saved), mime='text/csv', use_container_width=True
                        )
            with c2:
                if st.button("🔄  Retry Same Topic", use_container_width=True):
                    st.session_state.update({
                        "quiz_submitted": False, "quiz_generated": False,
                        "quiz_manager":   QuizManager()
                    })
                    with st.spinner("Re-generating..."):
                        gen = QuestionGenerator()
                        ok  = st.session_state.quiz_manager.generate_questions(gen, t, qt, d, n)
                    st.session_state.quiz_generated = ok
                    st.rerun()
            with c3:
                if st.button("🆕  New Quiz", use_container_width=True):
                    st.session_state.update({
                        "quiz_submitted": False, "quiz_generated": False,
                        "quiz_manager": QuizManager(), "c_topic": ""
                    })
                    st.rerun()


if __name__ == "__main__":
    main()