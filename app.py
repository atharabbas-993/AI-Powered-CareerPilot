import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os
from prompts import (
    SYSTEM_PROMPT,
    get_career_prompt,
    is_safe_input,
    is_safe_output
)
from domains import (
    get_all_domains,
    get_domain_info
)

# =====================================
# LOAD API KEY
# =====================================
load_dotenv()
try:
    api_key = st.secrets["GROQ_API_KEY"]
except:
    api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key)

# =====================================
# PAGE CONFIG
# =====================================
st.set_page_config(
    page_title="Pakistan AI Career Bot",
    page_icon="🤖",
    layout="wide"
)

# =====================================
# GLOBAL CSS
# =====================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;1,9..40,300&family=JetBrains+Mono:wght@400;500;600&display=swap');

/* ─── CSS VARIABLES ─── */
:root {
    --bg-base:       #060912;
    --bg-surface:    #0c1220;
    --bg-elevated:   #111827;
    --bg-card:       #0f1729;
    --accent-blue:   #1d6fce;
    --accent-red:    #c0392b;
    --accent-red-br: #e74c3c;
    --accent-blue-br:#3b8eea;
    --glow-blue:     rgba(29, 111, 206, 0.25);
    --glow-red:      rgba(192, 57, 43, 0.25);
    --text-primary:  #eef2ff;
    --text-secondary:#8b9cc8;
    --text-muted:    #4a5578;
    --border:        #1e2d4a;
    --border-bright: #2a3f66;
}

/* ─── BASE ─── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif !important;
    background-color: var(--bg-base) !important;
    color: var(--text-primary) !important;
}

.stApp {
    background:
        radial-gradient(ellipse 80% 50% at 10% 0%, rgba(29,111,206,0.12) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 90% 100%, rgba(192,57,43,0.10) 0%, transparent 60%),
        var(--bg-base) !important;
}

/* Hide streamlit branding */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem !important; max-width: 1200px; }

/* ─── HERO ─── */
.hero-wrap {
    text-align: center;
    padding: 2.5rem 1rem 1.5rem;
    animation: fadeDown 0.7s cubic-bezier(.16,1,.3,1) both;
}
.hero-eyebrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: var(--accent-red-br);
    margin-bottom: 0.7rem;
}
.hero-title {
    font-family: 'DM Serif Display', serif;
    font-size: 2.8rem;
    font-weight: 400;
    line-height: 1.15;
    color: var(--text-primary);
    margin-bottom: 0.6rem;
}
.hero-title span {
    background: linear-gradient(110deg, var(--accent-blue-br) 0%, var(--accent-red-br) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-sub {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.9rem;
    color: var(--text-secondary);
    font-weight: 300;
    letter-spacing: 0.3px;
}

/* ─── STEP TRACK ─── */
.step-track {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0;
    margin: 1.8rem auto 0.5rem;
    max-width: 520px;
}
.st-node {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.35rem;
}
.st-circle {
    width: 34px; height: 34px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    font-weight: 600;
    transition: all 0.4s ease;
}
.st-circle.done   { background: var(--accent-blue); color: #fff; box-shadow: 0 0 14px var(--glow-blue); }
.st-circle.active { background: linear-gradient(135deg, var(--accent-blue), var(--accent-red)); color: #fff; box-shadow: 0 0 20px var(--glow-red); }
.st-circle.idle   { background: var(--bg-elevated); color: var(--text-muted); border: 1px solid var(--border); }
.st-label {
    font-size: 0.65rem;
    font-family: 'JetBrains Mono', monospace;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: var(--text-muted);
}
.st-label.active-label { color: var(--accent-blue-br); }
.st-line {
    flex: 1;
    height: 1px;
    max-width: 80px;
    margin-bottom: 1.2rem;
    background: var(--border);
    transition: background 0.4s;
}
.st-line.done-line { background: linear-gradient(90deg, var(--accent-blue), var(--accent-red)); }

/* ─── SECTION HEADING ─── */
.sec-heading {
    font-family: 'DM Serif Display', serif;
    font-size: 1.6rem;
    color: var(--text-primary);
    margin-bottom: 0.3rem;
}
.sec-sub {
    font-size: 0.85rem;
    color: var(--text-secondary);
    margin-bottom: 1.8rem;
    font-weight: 300;
}

/* ─── DOMAIN CARDS ─── */
.d-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.4rem 1.2rem;
    height: 100%;
    transition: all 0.3s cubic-bezier(.4,0,.2,1);
    position: relative;
    overflow: hidden;
    animation: fadeUp 0.5s ease both;
}
.d-card::after {
    content: '';
    position: absolute;
    inset: 0;
    border-radius: 14px;
    background: linear-gradient(135deg, var(--glow-blue), var(--glow-red));
    opacity: 0;
    transition: opacity 0.3s ease;
}
.d-card:hover {
    border-color: var(--accent-blue);
    transform: translateY(-3px);
    box-shadow: 0 12px 35px var(--glow-blue);
}
.d-card:hover::after { opacity: 1; }
.d-icon { font-size: 1.9rem; margin-bottom: 0.7rem; position: relative; z-index: 1; }
.d-name {
    font-family: 'DM Serif Display', serif;
    font-size: 1rem;
    color: var(--text-primary);
    margin-bottom: 0.35rem;
    position: relative; z-index: 1;
}
.d-desc {
    font-size: 0.78rem;
    color: var(--text-secondary);
    line-height: 1.55;
    margin-bottom: 0.8rem;
    font-weight: 300;
    position: relative; z-index: 1;
}
.d-chip {
    display: inline-block;
    background: rgba(29,111,206,0.12);
    border: 1px solid rgba(29,111,206,0.3);
    color: var(--accent-blue-br);
    font-size: 0.66rem;
    font-family: 'JetBrains Mono', monospace;
    padding: 0.18rem 0.55rem;
    border-radius: 20px;
    margin: 0.15rem 0.15rem 0 0;
    position: relative; z-index: 1;
}

/* ─── SELECTED DOMAIN BANNER ─── */
.sel-banner {
    display: flex;
    align-items: center;
    gap: 1.2rem;
    background: linear-gradient(110deg, rgba(29,111,206,0.1) 0%, rgba(192,57,43,0.08) 100%);
    border: 1px solid var(--accent-blue);
    border-radius: 14px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 1.8rem;
    animation: fadeUp 0.4s ease both;
}
.sel-icon { font-size: 2.2rem; }
.sel-name {
    font-family: 'DM Serif Display', serif;
    font-size: 1.25rem;
    color: var(--text-primary);
}
.sel-desc {
    font-size: 0.8rem;
    color: var(--text-secondary);
    font-weight: 300;
    margin-top: 0.1rem;
}

/* ─── STATS ROW ─── */
.stats-row {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
    margin-bottom: 2rem;
}
.s-card {
    background: var(--bg-elevated);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1rem 1.2rem;
    text-align: center;
}
.s-val {
    font-family: 'DM Serif Display', serif;
    font-size: 1.6rem;
    background: linear-gradient(110deg, var(--accent-blue-br), var(--accent-red-br));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.s-lbl {
    font-size: 0.68rem;
    color: var(--text-muted);
    font-family: 'JetBrains Mono', monospace;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-top: 0.15rem;
}

/* ─── FORM ─── */
.form-card {
    background: var(--bg-surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 2rem;
    animation: fadeUp 0.5s ease 0.1s both;
}
.form-heading {
    font-family: 'DM Serif Display', serif;
    font-size: 1.3rem;
    color: var(--text-primary);
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    gap: 0.6rem;
}

/* ─── INPUTS ─── */
.stTextInput input,
.stSelectbox > div > div,
.stMultiSelect > div > div {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-bright) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.88rem !important;
}
.stTextInput input:focus {
    border-color: var(--accent-blue) !important;
    box-shadow: 0 0 0 2px var(--glow-blue) !important;
}
label, .stSelectbox label, .stMultiSelect label, .stTextInput label, .stRadio label {
    color: var(--text-secondary) !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.3px;
}

/* ─── BUTTONS ─── */
.stButton > button {
    background: linear-gradient(110deg, var(--accent-blue) 0%, #1a5bb0 100%) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    letter-spacing: 0.3px !important;
    padding: 0.55rem 1.4rem !important;
    transition: all 0.25s ease !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px var(--glow-blue) !important;
    background: linear-gradient(110deg, var(--accent-blue-br), var(--accent-blue)) !important;
}

/* ─── GENERATING SCREEN ─── */
.gen-wrap {
    text-align: center;
    padding: 4rem 1rem;
    animation: fadeUp 0.5s ease both;
}
.gen-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.8rem;
    color: var(--text-primary);
    margin: 1rem 0 0.5rem;
}
.gen-sub {
    color: var(--text-secondary);
    font-size: 0.85rem;
    font-weight: 300;
    font-family: 'JetBrains Mono', monospace;
}
.pulse-dot {
    display: inline-block;
    width: 10px; height: 10px;
    background: var(--accent-red-br);
    border-radius: 50%;
    margin: 0 4px;
    animation: pulse 1.2s ease-in-out infinite;
}
.pulse-dot:nth-child(2) { animation-delay: 0.2s; background: var(--accent-blue-br); }
.pulse-dot:nth-child(3) { animation-delay: 0.4s; }

/* ─── ROADMAP DISPLAY ─── */
.roadmap-wrap {
    background: var(--bg-surface);
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 2.2rem;
    margin: 1rem 0;
    animation: fadeUp 0.5s ease both;
    line-height: 1.8;
}

/* Claude-style typography for roadmap content */
.roadmap-wrap h1, .roadmap-wrap h2, .roadmap-wrap h3 {
    font-family: 'DM Serif Display', serif !important;
    color: var(--text-primary) !important;
}
.roadmap-wrap p, .roadmap-wrap li {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.92rem !important;
    color: var(--text-secondary) !important;
    line-height: 1.8 !important;
    font-weight: 300 !important;
}
.roadmap-wrap strong {
    color: var(--text-primary) !important;
    font-weight: 600 !important;
}
.roadmap-wrap code {
    font-family: 'JetBrains Mono', monospace !important;
    background: var(--bg-elevated) !important;
    border: 1px solid var(--border) !important;
    padding: 0.15rem 0.4rem !important;
    border-radius: 4px !important;
    font-size: 0.82rem !important;
    color: var(--accent-blue-br) !important;
}

/* Markdown rendered inside st.markdown for roadmap */
.element-container .stMarkdown p {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.92rem !important;
    color: var(--text-secondary) !important;
    line-height: 1.8 !important;
    font-weight: 300 !important;
}
.element-container .stMarkdown h1,
.element-container .stMarkdown h2,
.element-container .stMarkdown h3 {
    font-family: 'DM Serif Display', serif !important;
    color: var(--text-primary) !important;
}
.element-container .stMarkdown li {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.9rem !important;
    color: var(--text-secondary) !important;
    line-height: 1.75 !important;
}

/* ─── ROADMAP HEADER ─── */
.roadmap-hdr {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1.8rem;
    padding-bottom: 1.2rem;
    border-bottom: 1px solid var(--border);
}
.roadmap-hdr-icon { font-size: 2.4rem; }
.roadmap-hdr-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.4rem;
    color: var(--text-primary);
}
.roadmap-hdr-sub {
    font-size: 0.78rem;
    color: var(--text-muted);
    font-family: 'JetBrains Mono', monospace;
    margin-top: 0.1rem;
}

/* ─── CHAT ─── */
[data-testid="stChatMessage"] {
    background: var(--bg-elevated) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    margin-bottom: 0.8rem !important;
}
[data-testid="stChatMessage"] p {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.9rem !important;
    color: var(--text-secondary) !important;
    line-height: 1.7 !important;
}
.stChatInput > div {
    background: var(--bg-elevated) !important;
    border: 1px solid var(--border-bright) !important;
    border-radius: 12px !important;
}

/* ─── DOWNLOAD BUTTON ─── */
.stDownloadButton > button {
    background: linear-gradient(110deg, var(--accent-red) 0%, #a93226 100%) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    transition: all 0.25s ease !important;
}
.stDownloadButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px var(--glow-red) !important;
}

/* ─── PROGRESS BAR ─── */
.stProgress > div > div > div {
    background: linear-gradient(90deg, var(--accent-blue), var(--accent-red-br)) !important;
    border-radius: 4px !important;
}

/* ─── DIVIDER ─── */
hr { border-color: var(--border) !important; }

/* ─── SIDEBAR ─── */
[data-testid="stSidebar"] {
    background: var(--bg-surface) !important;
    border-right: 1px solid var(--border) !important;
}

/* ─── SCROLLBAR ─── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: var(--bg-base); }
::-webkit-scrollbar-thumb { background: var(--border-bright); border-radius: 3px; }

/* ─── FOOTER ─── */
.footer {
    text-align: center;
    padding: 2rem 0 1rem;
    border-top: 1px solid var(--border);
    margin-top: 3rem;
    color: var(--text-muted);
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.5px;
}

/* ─── ANIMATIONS ─── */
@keyframes fadeDown {
    from { opacity: 0; transform: translateY(-20px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50%       { opacity: 0.4; transform: scale(0.75); }
}
@keyframes spin {
    to { transform: rotate(360deg); }
}

/* stagger domain cards */
.d-card:nth-child(1){animation-delay:.05s}
.d-card:nth-child(2){animation-delay:.10s}
.d-card:nth-child(3){animation-delay:.15s}
.d-card:nth-child(4){animation-delay:.20s}
.d-card:nth-child(5){animation-delay:.25s}
.d-card:nth-child(6){animation-delay:.30s}
.d-card:nth-child(7){animation-delay:.35s}
.d-card:nth-child(8){animation-delay:.40s}

/* warning / error */
.stAlert { border-radius: 10px !important; }
</style>
""", unsafe_allow_html=True)

# =====================================
# DOMAIN ICONS
# =====================================
DOMAIN_ICONS = {
    "Machine Learning Engineer":  "🧠", 
    "Deep Learning Engineer":     "⚡",
    "Computer Vision Engineer":   "👁️",
    "NLP Engineer":               "💬",
    "MLOps Engineer":             "⚙️",
    "Data Scientist":             "📊",
    "Generative AI Engineer":     "✨",
    "AI Research Engineer":       "🔬"
}

# =====================================
# SESSION STATE
# =====================================
defaults = {
    "messages": [{"role": "system", "content": SYSTEM_PROMPT}],
    "roadmap_generated": False,
    "selected_domain": None,
    "roadmap_text": "",
    "current_step": 1,
    "student_name": "",
    "form_data": {}
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# =====================================
# HERO
# =====================================
st.markdown("""
<div class="hero-wrap">
    <div class="hero-eyebrow">● Pakistan AI Career Roadmap Bot</div>
    <div class="hero-title">Find Your Path in <span>Artificial Intelligence</span></div>
    <div class="hero-sub">AI-powered personalized learning roadmaps for students — by Athar Abbas</div>
</div>
""", unsafe_allow_html=True)

# =====================================
# STEP TRACKER
# =====================================
step = st.session_state.current_step
labels = ["Domain", "Profile", "Generating", "Roadmap"]

def sc(n):   # circle class
    if n < step:  return "done"
    if n == step: return "active"
    return "idle"

def lc(n):   # line class
    return "done-line" if n < step else ""

nodes_html = ""
for i, lbl in enumerate(labels, 1):
    nodes_html += f'<div class="st-node"><div class="st-circle {sc(i)}">{i}</div><div class="st-label {"active-label" if i==step else ""}">{lbl}</div></div>'
    if i < len(labels):
        nodes_html += f'<div class="st-line {lc(i)}"></div>'

st.markdown(f'<div class="step-track">{nodes_html}</div>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# ======================================================
# STEP 1 — CHOOSE DOMAIN
# ======================================================
if step == 1:
    st.markdown('<div class="sec-heading">Choose Your AI Domain</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-sub">Select the specialisation that excites you most — we\'ll build a roadmap around it.</div>', unsafe_allow_html=True)

    all_domains = get_all_domains()
    cols = st.columns(4)

    for i, dname in enumerate(all_domains):
        dinfo = get_domain_info(dname)
        icon  = DOMAIN_ICONS.get(dname, "🤖")
        chips = "".join([f'<span class="d-chip">{s}</span>'
                         for s in dinfo["skills_required"][:3]])

        with cols[i % 4]:
            st.markdown(f"""
            <div class="d-card">
                <div class="d-icon">{icon}</div>
                <div class="d-name">{dname}</div>
                <div class="d-desc">{dinfo['description']}</div>
                <div>{chips}</div>
            </div>
            """, unsafe_allow_html=True)

            if st.button(f"Select  {icon}", key=f"d{i}", use_container_width=True):
                st.session_state.selected_domain = dname
                st.session_state.current_step    = 2
                st.rerun()

# ======================================================
# STEP 2 — STUDENT PROFILE
# ======================================================
elif step == 2:
    dinfo = get_domain_info(st.session_state.selected_domain)
    icon  = DOMAIN_ICONS.get(st.session_state.selected_domain, "🤖")

    # Banner
    st.markdown(f"""
    <div class="sel-banner">
        <span class="sel-icon">{icon}</span>
        <div>
            <div class="sel-name">{st.session_state.selected_domain}</div>
            <div class="sel-desc">{dinfo['description']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Stats (no salary, no duration)
    st.markdown(f"""
    <div class="stats-row">
        <div class="s-card">
            <div class="s-val">{len(dinfo['skills_required'])}</div>
            <div class="s-lbl">Core Skills</div>
        </div>
        <div class="s-card">
            <div class="s-val">{len(dinfo['free_resources'])}</div>
            <div class="s-lbl">Free Resources</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Form
    st.markdown('<div class="form-card">', unsafe_allow_html=True)
    st.markdown('<div class="form-heading">👤 Tell Us About Yourself</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Your Good Name", placeholder="e.g. Athar Abbas")
        education = st.selectbox("Current Education", [
            "Matric / O-Levels",
            "FSc / A-Levels",
            "BS CS/IT/AI — 1st Semester",
            "BS CS/IT/AI — 2nd Semester",
            "BS CS/IT/AI — 3rd Semester",
            "BS CS/IT/AI — 4th Semester",
            "BS CS/IT/AI — 5th Semester",
            "BS CS/IT/AI — 6th Semester",
            "BS CS/IT/AI — 7th Semester",
            "BS CS/IT/AI — 8th Semester",
            "Fresh Graduate",
            "Working Professional",
            "Other"
        ])
    with col2:
        experience = st.selectbox("Coding Experience Level", [
            "Complete Beginner — No experience",
            "Beginner — Less than 6 months",
            "Intermediate — 6 months to 1 year",
            "Solid — 1 to 2 years",
            "Experienced — 2+ years"
        ])
        skills = st.multiselect("Your Current Skills", [
            "Python Basics",
            "Python Advanced",
            "Mathematics",
            "Statistics",
            "Machine Learning Basics",
            "Deep Learning",
            "Data Analysis",
            "SQL",
            "Web Development",
            "No Skills Yet"
        ])

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2 = st.columns([1, 3])
    with c1:
        if st.button("← Back", use_container_width=True):
            st.session_state.current_step = 1
            st.rerun()
    with c2:
        if st.button("🚀  Generate My Roadmap", use_container_width=True):
            if not name.strip():
                st.warning("⚠️  Please enter your name to continue.")
            else:
                st.session_state.student_name = name.strip()
                st.session_state.form_data = {
                    "name":       name.strip(),
                    "education":  education,
                    "skills":     skills,
                    "experience": experience
                }
                st.session_state.current_step = 3
                st.rerun()

# ======================================================
# STEP 3 — GENERATING
# ======================================================
elif step == 3:
    st.markdown("""
    <div class="gen-wrap">
        <div style="font-size:3.5rem;animation:fadeUp 0.4s ease both">⚡</div>
        <div class="gen-title">Building Your Roadmap</div>
        <div class="gen-sub">Analysing profile · cross-checking recommendations · writing plan</div>
        <div style="margin-top:1.2rem">
            <span class="pulse-dot"></span>
            <span class="pulse-dot"></span>
            <span class="pulse-dot"></span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    progress_bar = st.progress(0, text="Initialising…")
    form = st.session_state.form_data

    career_prompt = get_career_prompt(
        name       = form["name"],
        education  = form["education"],
        skills     = ", ".join(form["skills"]) if form["skills"] else "No skills yet",
        domain     = st.session_state.selected_domain,
        experience = form["experience"]
    )

    if not is_safe_input(career_prompt):
        st.error("⚠️  Invalid input detected.")
        st.session_state.current_step = 2
        st.rerun()

    st.session_state.messages.append({"role": "user", "content": career_prompt})

    responses = []
    for i in range(3):
        pct  = (i + 1) * 30
        msgs = [f"Generating roadmap — pass {i+1}/3…",
                "Cross-checking domain knowledge…",
                "Selecting best response…"]
        progress_bar.progress(pct, text=msgs[i])

        resp = client.chat.completions.create(
            model      = "llama-3.1-8b-instant",
            messages   = st.session_state.messages,
            temperature= 0.3,
            max_tokens = 2000
        )
        responses.append(resp.choices[0].message.content)

    progress_bar.progress(100, text="✅  Done!")

    best = max(responses, key=len)

    if not is_safe_output(best):
        st.error("⚠️  Something went wrong. Please try again.")
        st.session_state.current_step = 2
    else:
        st.session_state.messages.append({"role": "assistant", "content": best})
        st.session_state.roadmap_text     = best
        st.session_state.roadmap_generated= True
        st.session_state.current_step     = 4
        st.rerun()

# ======================================================
# STEP 4 — ROADMAP DISPLAY
# ======================================================
elif step == 4:
    icon  = DOMAIN_ICONS.get(st.session_state.selected_domain, "🤖")
    dinfo = get_domain_info(st.session_state.selected_domain)
    name  = st.session_state.student_name

    # Top row: title + download
    col_hdr, col_dl = st.columns([3, 1])
    with col_hdr:
        st.markdown(f"""
        <div class="roadmap-hdr">
            <span class="roadmap-hdr-icon">{icon}</span>
            <div>
                <div class="roadmap-hdr-title">{st.session_state.selected_domain}</div>
                <div class="roadmap-hdr-sub">Roadmap for {name}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_dl:
        download_content = (
            f"AI CAREER ROADMAP\n"
            f"For: {name}\n"
            f"Domain: {st.session_state.selected_domain}\n"
            f"{'─'*50}\n\n"
            f"{st.session_state.roadmap_text}\n\n"
            f"{'─'*50}\n"
            f"Generated by AI Career Roadmap Bot\n"
        )
        st.markdown("<br>", unsafe_allow_html=True)
        st.download_button(
            label    = "⬇️  Download Roadmap",
            data     = download_content,
            file_name= f"AI_Roadmap_{name.replace(' ','_')}.txt",
            mime     = "text/plain",
            use_container_width=True
        )

    # Stats (no salary, no duration)
    st.markdown(f"""
    <div class="stats-row">
        <div class="s-card">
            <div class="s-val">{len(dinfo['skills_required'])}</div>
            <div class="s-lbl">Skills in Roadmap</div>
        </div>
        <div class="s-card">
            <div class="s-val">{len(dinfo['pakistani_companies'])}</div>
            <div class="s-lbl">Hiring Companies</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Roadmap content — styled like Claude output
    st.markdown('<div class="roadmap-wrap">', unsafe_allow_html=True)
    st.markdown(st.session_state.roadmap_text)
    st.markdown("</div>", unsafe_allow_html=True)

    st.divider()

    # ── Follow-up chat ──
    st.markdown('<div class="sec-heading" style="font-size:1.2rem">💬 Ask Follow-up Questions</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-sub">Have questions about your roadmap? Ask anything below.</div>', unsafe_allow_html=True)

    # show only follow-up messages (skip system + initial roadmap exchange)
    for msg in st.session_state.messages[3:]:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_q = st.chat_input("Ask about resources, skills, companies…")
    if user_q:
        if not is_safe_input(user_q):
            st.error("⚠️  Please ask career-related questions only.")
        else:
            st.session_state.messages.append({"role": "user", "content": user_q})
            with st.spinner("Thinking…"):
                resp = client.chat.completions.create(
                    model      = "llama-3.1-8b-instant",
                    messages   = st.session_state.messages,
                    temperature= 0.3,
                    max_tokens = 1000
                )
                reply = resp.choices[0].message.content
            if not is_safe_output(reply):
                st.error("⚠️  Something went wrong.")
            else:
                st.session_state.messages.append({"role": "assistant", "content": reply})
                st.rerun()

    st.divider()

    # Action buttons
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🔄  New Roadmap", use_container_width=True):
            for k, v in defaults.items():
                st.session_state[k] = v
            st.rerun()
    with c2:
        if st.button("🔀  Change Domain", use_container_width=True):
            st.session_state.messages          = [{"role": "system", "content": SYSTEM_PROMPT}]
            st.session_state.roadmap_generated = False
            st.session_state.roadmap_text      = ""
            st.session_state.selected_domain   = None
            st.session_state.current_step      = 1
            st.rerun()

# ── FOOTER ──
st.markdown("""
<div class="footer">
    © 2026 Athar Abbas AI Engineer

</div>  
""", unsafe_allow_html=True)
