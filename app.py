import streamlit as st
import requests

st.set_page_config(
    page_title="AgriConnect",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
    --soil: #3d2b1f;
    --bark: #5c3d2e;
    --leaf: #2d6a4f;
    --sprout: #40916c;
    --mint: #74c69d;
    --sky: #e8f5e9;
    --cream: #fdf6ec;
    --sand: #f5e6d3;
    --terracotta: #c0714f;
    --gold: #d4a017;
    --text-dark: #1a1008;
    --text-mid: #3d2b1f;
    --text-light: #6b5344;
    --white: #ffffff;
}

* { font-family: 'DM Sans', sans-serif !important; }

html, body, .stApp {
    background-color: var(--cream) !important;
    background-image:
        radial-gradient(ellipse at 10% 0%, rgba(116,198,157,0.12) 0%, transparent 60%),
        radial-gradient(ellipse at 90% 100%, rgba(45,106,79,0.10) 0%, transparent 60%);
}

/* ─── SIDEBAR ─── */
section[data-testid="stSidebar"] {
    background: linear-gradient(175deg, var(--soil) 0%, var(--bark) 60%, #7a5230 100%) !important;
    border-right: 3px solid var(--gold);
}
section[data-testid="stSidebar"]::before {
    content: "";
    position: absolute;
    inset: 0;
    background-image: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.03'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
    pointer-events: none;
}
section[data-testid="stSidebar"] * { color: var(--sand) !important; }

.sidebar-brand {
    text-align: center;
    padding: 20px 0 10px;
}
.sidebar-brand h1 {
    font-family: 'Playfair Display', serif !important;
    font-size: 28px !important;
    font-weight: 900 !important;
    color: var(--gold) !important;
    letter-spacing: 1px;
    margin: 0;
}
.sidebar-brand p {
    font-size: 11px !important;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--mint) !important;
    margin-top: 4px;
}
.sidebar-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--gold), transparent);
    margin: 12px 0 20px;
}

.stRadio > div { gap: 4px !important; }
.stRadio > div > label {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.10) !important;
    border-radius: 10px !important;
    padding: 10px 14px !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    transition: all 0.2s ease !important;
    color: var(--sand) !important;
}
.stRadio > div > label:hover {
    background: rgba(212,160,23,0.20) !important;
    border-color: var(--gold) !important;
}
[data-baseweb="radio"] input:checked + div + span {
    color: var(--gold) !important;
}

/* ─── HERO BANNER ─── */
.hero-banner {
    background: linear-gradient(135deg, var(--leaf) 0%, var(--sprout) 50%, #1b4332 100%);
    padding: 44px 40px;
    border-radius: 24px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 12px 48px rgba(45,106,79,0.30);
}
.hero-banner::before {
    content: "🌾";
    position: absolute;
    right: 40px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 100px;
    opacity: 0.15;
}
.hero-banner::after {
    content: "";
    position: absolute;
    bottom: -30px;
    left: -30px;
    width: 160px;
    height: 160px;
    background: rgba(255,255,255,0.05);
    border-radius: 50%;
}
.hero-eyebrow {
    font-size: 11px;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: var(--mint);
    font-weight: 600;
    margin-bottom: 8px;
}
.hero-title {
    font-family: 'Playfair Display', serif !important;
    font-size: 48px !important;
    font-weight: 900 !important;
    color: #ffffff !important;
    margin: 0 0 10px !important;
    line-height: 1.1;
}
.hero-sub {
    font-size: 15px;
    color: rgba(255,255,255,0.78);
    font-weight: 300;
    max-width: 500px;
    line-height: 1.6;
}

/* ─── STAT CARDS ─── */
.stat-row { display: flex; gap: 16px; margin-bottom: 28px; }
.stat-card {
    flex: 1;
    background: var(--white);
    border-radius: 18px;
    padding: 22px 20px;
    text-align: center;
    box-shadow: 0 4px 20px rgba(61,43,31,0.08);
    border-top: 4px solid var(--gold);
    position: relative;
    overflow: hidden;
}
.stat-card::after {
    content: "";
    position: absolute;
    bottom: -20px;
    right: -20px;
    width: 80px;
    height: 80px;
    background: rgba(116,198,157,0.10);
    border-radius: 50%;
}
.stat-num {
    font-family: 'Playfair Display', serif !important;
    font-size: 36px !important;
    font-weight: 900 !important;
    color: var(--leaf) !important;
    line-height: 1;
    margin-bottom: 4px;
}
.stat-label {
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: var(--text-light) !important;
}

/* ─── FEATURE CARDS ─── */
.feature-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-top: 8px; }
.feature-card {
    background: var(--white);
    border-radius: 18px;
    padding: 22px 20px;
    box-shadow: 0 4px 18px rgba(61,43,31,0.07);
    border: 1.5px solid rgba(116,198,157,0.25);
    transition: transform 0.2s, box-shadow 0.2s;
    position: relative;
    overflow: hidden;
}
.feature-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 30px rgba(45,106,79,0.14);
}
.feature-card::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 4px;
    background: linear-gradient(90deg, var(--leaf), var(--mint));
    border-radius: 18px 18px 0 0;
}
.feature-icon { font-size: 28px; margin-bottom: 10px; }
.feature-title {
    font-family: 'Playfair Display', serif !important;
    font-size: 16px !important;
    font-weight: 700 !important;
    color: var(--text-dark) !important;
    margin-bottom: 4px;
}
.feature-desc { font-size: 13px; color: var(--text-light) !important; line-height: 1.5; }

/* ─── SECTION HEADERS ─── */
.section-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 20px;
}
.section-header h2 {
    font-family: 'Playfair Display', serif !important;
    font-size: 28px !important;
    font-weight: 700 !important;
    color: var(--text-dark) !important;
    margin: 0 !important;
}
.section-pill {
    background: linear-gradient(90deg, var(--leaf), var(--sprout));
    color: white !important;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    padding: 4px 12px;
    border-radius: 20px;
}
.page-subtitle {
    font-size: 14px;
    color: var(--text-light) !important;
    margin-bottom: 24px;
    font-weight: 300;
    letter-spacing: 0.3px;
}
hr { border-color: rgba(116,198,157,0.25) !important; }

/* ─── CHAT ─── */
.chat-container {
    background: var(--white);
    border-radius: 20px;
    padding: 24px;
    min-height: 300px;
    box-shadow: 0 4px 20px rgba(61,43,31,0.07);
    border: 1.5px solid rgba(116,198,157,0.2);
    margin-bottom: 16px;
}
.chat-user {
    background: linear-gradient(135deg, var(--leaf), var(--sprout));
    color: white !important;
    padding: 12px 18px;
    border-radius: 20px 20px 4px 20px;
    margin: 10px 0 10px auto;
    max-width: 75%;
    font-size: 14px;
    line-height: 1.5;
    box-shadow: 0 4px 12px rgba(45,106,79,0.25);
    display: table;
    margin-left: auto;
}
.chat-ai {
    background: var(--sand);
    color: var(--text-dark) !important;
    padding: 12px 18px;
    border-radius: 20px 20px 20px 4px;
    margin: 10px 0;
    max-width: 75%;
    font-size: 14px;
    line-height: 1.5;
    border: 1px solid rgba(116,198,157,0.30);
    box-shadow: 0 2px 8px rgba(61,43,31,0.06);
}
.chat-label {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 4px;
}
.chat-label.ai-label { color: var(--leaf) !important; }
.chat-label.user-label { color: rgba(255,255,255,0.7) !important; text-align: right; }

/* ─── BUTTONS ─── */
.stButton > button {
    background: linear-gradient(135deg, var(--leaf) 0%, var(--sprout) 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    padding: 10px 24px !important;
    letter-spacing: 0.5px;
    box-shadow: 0 4px 16px rgba(45,106,79,0.30) !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 22px rgba(45,106,79,0.40) !important;
}

/* ─── INPUTS ─── */
.stTextInput > div > div > input,
.stSelectbox > div > div {
    border-radius: 12px !important;
    border: 2px solid rgba(116,198,157,0.35) !important;
    background: var(--white) !important;
    color: var(--text-dark) !important;
    font-size: 14px !important;
}
.stTextInput > div > div > input:focus,
.stSelectbox > div > div:focus {
    border-color: var(--sprout) !important;
    box-shadow: 0 0 0 3px rgba(64,145,108,0.15) !important;
}
label, .stSelectbox label, .stTextInput label { color: var(--text-mid) !important; font-weight: 500 !important; font-size: 13px !important; }

/* ─── MARKETPLACE ─── */
.market-card {
    background: var(--white);
    border-radius: 18px;
    padding: 20px;
    margin-bottom: 14px;
    box-shadow: 0 4px 16px rgba(61,43,31,0.07);
    border: 1.5px solid rgba(116,198,157,0.20);
    display: flex;
    gap: 14px;
    align-items: flex-start;
    position: relative;
    overflow: hidden;
}
.market-card::after {
    content: "";
    position: absolute;
    top: 0; right: 0;
    width: 60px; height: 60px;
    background: rgba(116,198,157,0.07);
    border-radius: 0 18px 0 60px;
}
.market-icon-wrap {
    width: 52px; height: 52px;
    background: var(--sky);
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 26px;
    flex-shrink: 0;
}
.market-title {
    font-weight: 700;
    font-size: 15px;
    color: var(--text-dark) !important;
    margin-bottom: 4px;
}
.market-price {
    font-size: 13px;
    color: var(--leaf) !important;
    font-weight: 700;
}
.market-seller { font-size: 12px; color: var(--text-light) !important; }
.market-badge {
    background: var(--gold);
    color: var(--text-dark) !important;
    font-size: 11px;
    font-weight: 700;
    padding: 2px 8px;
    border-radius: 8px;
}

/* ─── SCHEME CARDS ─── */
.scheme-card {
    background: var(--white);
    border-radius: 18px;
    padding: 22px;
    margin-bottom: 14px;
    box-shadow: 0 4px 16px rgba(61,43,31,0.07);
    border-left: 5px solid var(--gold);
    position: relative;
}
.scheme-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 10px; }
.scheme-title { font-family: 'Playfair Display', serif !important; font-size: 18px !important; font-weight: 700 !important; color: var(--text-dark) !important; }
.scheme-amount {
    background: linear-gradient(135deg, var(--leaf), var(--sprout));
    color: white !important;
    font-size: 12px;
    font-weight: 700;
    padding: 4px 12px;
    border-radius: 20px;
    white-space: nowrap;
}
.scheme-desc { font-size: 13px; color: var(--text-light) !important; margin-bottom: 10px; line-height: 1.5; }
.scheme-detail { font-size: 12px; color: var(--text-mid) !important; margin-bottom: 4px; }
.scheme-detail b { color: var(--bark) !important; }

/* ─── SURVEY ─── */
.survey-card {
    background: var(--white);
    border-radius: 20px;
    padding: 28px;
    box-shadow: 0 4px 20px rgba(61,43,31,0.07);
    border: 1.5px solid rgba(116,198,157,0.20);
    margin-bottom: 20px;
}
.step-card {
    background: linear-gradient(135deg, var(--sky), #d8f3dc);
    border-radius: 14px;
    padding: 14px 18px;
    margin-bottom: 10px;
    border-left: 4px solid var(--leaf);
}
.step-text { color: var(--text-dark) !important; font-size: 14px; font-weight: 500; }
.step-num {
    background: var(--leaf);
    color: white !important;
    width: 24px; height: 24px;
    border-radius: 50%;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    font-weight: 700;
    margin-right: 10px;
}

/* ─── UPLOAD ZONE ─── */
.stFileUploader {
    border: 2px dashed rgba(116,198,157,0.5) !important;
    border-radius: 16px !important;
    background: rgba(232,245,233,0.4) !important;
    padding: 12px !important;
}

/* ─── HIDE STREAMLIT DEFAULTS ─── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 24px !important; padding-bottom: 40px !important; max-width: 1100px !important; }

/* ─── PAGE TITLE BAR ─── */
.page-title-bar {
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 6px;
}
.page-icon-circle {
    width: 48px; height: 48px;
    background: linear-gradient(135deg, var(--leaf), var(--sprout));
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
    box-shadow: 0 4px 14px rgba(45,106,79,0.30);
}
.page-title-text {
    font-family: 'Playfair Display', serif !important;
    font-size: 32px !important;
    font-weight: 900 !important;
    color: var(--text-dark) !important;
    margin: 0 !important;
}
</style>
""", unsafe_allow_html=True)

# ─── SIDEBAR ──────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <h1>AgriConnect</h1>
        <p>Smart Farming Platform</p>
    </div>
    <div class="sidebar-divider"></div>
    """, unsafe_allow_html=True)

    page = st.radio("", [
        "🏠  Home",
        "🤖  AI Assistant",
        "🌿  Disease Detection",
        "🛒  Marketplace",
        "🏛️  Government Schemes",
        "📋  Smart Survey",
    ], label_visibility="collapsed")

    st.markdown("""
    <div style="position:fixed;bottom:24px;left:0;width:260px;padding:0 20px;box-sizing:border-box;">
        <div style="background:rgba(255,255,255,0.07);border:1px solid rgba(255,255,255,0.12);border-radius:14px;padding:14px;text-align:center;">
            <div style="font-size:11px;letter-spacing:1.5px;text-transform:uppercase;color:rgba(232,230,220,0.6);margin-bottom:4px;">Powered by</div>
            <div style="font-family:'Playfair Display',serif;font-size:15px;font-weight:700;color:#d4a017;">AI × Agriculture</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# HOME
# ═══════════════════════════════════════════════════════
if page == "🏠  Home":
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-eyebrow">🌱 Welcome to AgriConnect</div>
        <div class="hero-title">Grow Smarter,<br>Earn Better.</div>
        <div class="hero-sub">Your AI-powered smart farming companion — bringing technology to every field, every farmer, every harvest.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="stat-row">
        <div class="stat-card">
            <div class="stat-num">500+</div>
            <div class="stat-label">Farmers Helped</div>
        </div>
        <div class="stat-card">
            <div class="stat-num">95%</div>
            <div class="stat-label">Success Rate</div>
        </div>
        <div class="stat-card">
            <div class="stat-num">24/7</div>
            <div class="stat-label">AI Support</div>
        </div>
        <div class="stat-card">
            <div class="stat-num">6+</div>
            <div class="stat-label">Govt. Schemes</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="display:flex;align-items:center;gap:12px;margin-bottom:20px;">
        <h3 style="font-family:'Playfair Display',serif;font-size:22px;font-weight:700;color:#1a1008;margin:0;">Our Features</h3>
        <div style="height:1px;flex:1;background:linear-gradient(90deg,rgba(116,198,157,0.5),transparent);"></div>
    </div>
    <div class="feature-grid">
        <div class="feature-card">
            <div class="feature-icon">🤖</div>
            <div class="feature-title">AI Assistant</div>
            <div class="feature-desc">Get instant answers on crops, pests, soil health, and weather — powered by advanced AI.</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">🌿</div>
            <div class="feature-title">Disease Detection</div>
            <div class="feature-desc">Upload a leaf photo and get instant disease diagnosis with treatment recommendations.</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">🛒</div>
            <div class="feature-title">Marketplace</div>
            <div class="feature-desc">Buy quality seeds, rent farm equipment, and connect directly with buyers near you.</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">🏛️</div>
            <div class="feature-title">Government Schemes</div>
            <div class="feature-desc">Discover and apply for PM-KISAN, crop insurance, Kisan Credit Card and more.</div>
        </div>
        <div class="feature-card" style="grid-column: span 2;">
            <div class="feature-icon">📋</div>
            <div class="feature-title">Smart Survey</div>
            <div class="feature-desc">Answer a quick survey and receive a personalized step-by-step farm roadmap tailored to your land, water source, and goals.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# AI ASSISTANT
# ═══════════════════════════════════════════════════════
elif page == "🤖  AI Assistant":
    st.markdown("""
    <div class="page-title-bar">
        <div class="page-icon-circle">🤖</div>
        <h1 class="page-title-text">AI Assistant</h1>
    </div>
    <div class="page-subtitle">Ask anything about farming, crops, pests, soil, or weather.</div>
    """, unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "ai", "content": "🌱 Namaste! I'm your AgriConnect AI. Ask me anything about your farm — crops, soil, pests, weather, or government schemes!"}
        ]

    with st.container():
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(f"""
                <div style="text-align:right;">
                    <div class="chat-label user-label" style="color:#5c7c6a">You</div>
                    <div class="chat-user">{msg["content"]}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div>
                    <div class="chat-label ai-label">🌿 AgriConnect AI</div>
                    <div class="chat-ai">{msg["content"]}</div>
                </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    col_input, col_btn = st.columns([5, 1])
    with col_input:
        user_input = st.text_input("", placeholder="e.g. My tomato leaves are turning yellow — what should I do?", key="chat_input", label_visibility="collapsed")
    with col_btn:
        send = st.button("Send ➤")

    if send and user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        try:
            res = requests.post("http://localhost:8000/chat", json={"message": user_input})
            reply = res.json()["reply"]
        except:
            reply = "⚠️ Could not connect to the server. Please make sure the backend is running."
        st.session_state.messages.append({"role": "ai", "content": reply})
        st.rerun()

# ═══════════════════════════════════════════════════════
# DISEASE DETECTION
# ═══════════════════════════════════════════════════════
elif page == "🌿  Disease Detection":
    st.markdown("""
    <div class="page-title-bar">
        <div class="page-icon-circle">🌿</div>
        <h1 class="page-title-text">Disease Detection</h1>
    </div>
    <div class="page-subtitle">Upload a clear photo of the affected leaf for instant AI diagnosis.</div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1], gap="large")
    with col1:
        st.markdown('<div class="survey-card">', unsafe_allow_html=True)
        st.markdown('<div style="font-weight:600;color:#3d2b1f;margin-bottom:12px;font-size:15px;">📸 Upload Leaf Photo</div>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Choose image (JPG/PNG)", type=["jpg","jpeg","png"], label_visibility="collapsed")
        if uploaded_file:
            st.image(uploaded_file, caption="Uploaded leaf", use_column_width=True)
            if st.button("🔍 Analyze Leaf Disease"):
                with st.spinner("Analyzing your crop leaf with AI..."):
                    try:
                        res = requests.post(
                            "http://localhost:8000/disease",
                            files={"file": ("image.jpg", uploaded_file.getvalue(), "image/jpeg")}
                        )
                        data = res.json()
                        st.markdown(f"""
                        <div style="background:#fff5f5;border:2px solid #fca5a5;border-radius:14px;padding:16px;margin-top:12px;">
                            <div style="font-weight:700;color:#dc2626;font-size:14px;">🦠 Detected Disease</div>
                            <div style="font-size:18px;font-weight:700;color:#1a1008;margin-top:4px;">{data['disease']}</div>
                        </div>
                        <div style="background:#f0fdf4;border:2px solid #86efac;border-radius:14px;padding:16px;margin-top:10px;">
                            <div style="font-weight:700;color:#16a34a;font-size:14px;">💊 Recommended Treatment</div>
                            <div style="font-size:14px;color:#1a1008;margin-top:4px;line-height:1.5;">{data['cure']}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    except:
                        st.error("Could not connect to server. Please ensure backend is running.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="survey-card">
            <div style="font-weight:600;color:#3d2b1f;margin-bottom:14px;font-size:15px;">💡 Tips for Best Results</div>
            <div class="step-card"><div class="step-text"><span class="step-num">1</span>Take photo in natural daylight</div></div>
            <div class="step-card"><div class="step-text"><span class="step-num">2</span>Ensure the leaf fills most of the frame</div></div>
            <div class="step-card"><div class="step-text"><span class="step-num">3</span>Capture both sides of the leaf if possible</div></div>
            <div class="step-card"><div class="step-text"><span class="step-num">4</span>Use a clean, plain background</div></div>
            <div class="step-card"><div class="step-text"><span class="step-num">5</span>Avoid blurry or heavily shadowed images</div></div>
        </div>
        """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# MARKETPLACE
# ═══════════════════════════════════════════════════════
elif page == "🛒  Marketplace":
    st.markdown("""
    <div class="page-title-bar">
        <div class="page-icon-circle">🛒</div>
        <h1 class="page-title-text">Marketplace</h1>
    </div>
    <div class="page-subtitle">Buy seeds, rent farm equipment, and connect directly with buyers.</div>
    """, unsafe_allow_html=True)

    col_f, col_s = st.columns([1, 2])
    with col_f:
        category = st.selectbox("Filter by Category", ["All", "Seeds", "Tools", "Rental", "Buyers"])
    with col_s:
        search = st.text_input("Search products...", placeholder="e.g. tomato seeds, tractor...")

    products = [
        {"icon": "🌱", "title": "Tomato Seeds (Hybrid)", "category": "Seeds", "price": "₹120/pack", "seller": "Ravi Farms", "rating": "⭐ 4.8"},
        {"icon": "🌾", "title": "Ragi Seeds (Organic)", "category": "Seeds", "price": "₹80/kg", "seller": "Green Valley", "rating": "⭐ 4.6"},
        {"icon": "🚜", "title": "Tractor Rental", "category": "Rental", "price": "₹800/day", "seller": "Kumar Tractors", "rating": "⭐ 4.9"},
        {"icon": "💧", "title": "Drip Irrigation Kit", "category": "Tools", "price": "₹2,500", "seller": "IrriTech", "rating": "⭐ 4.7"},
        {"icon": "🔧", "title": "Hand Weeder", "category": "Tools", "price": "₹350", "seller": "FarmTools Co", "rating": "⭐ 4.4"},
        {"icon": "🏪", "title": "Direct Vegetable Buyer", "category": "Buyers", "price": "Best Price", "seller": "FreshMart", "rating": "⭐ 4.8"},
    ]

    filtered = [p for p in products if (category == "All" or p["category"] == category) and (search.lower() in p["title"].lower())]
    st.markdown(f'<div style="font-size:13px;color:#6b5344;margin:12px 0;">{len(filtered)} product(s) found</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    for i, p in enumerate(filtered):
        with col1 if i % 2 == 0 else col2:
            st.markdown(f"""
            <div class="market-card">
                <div class="market-icon-wrap">{p["icon"]}</div>
                <div style="flex:1;">
                    <div class="market-title">{p["title"]}</div>
                    <div style="display:flex;gap:8px;align-items:center;margin:4px 0;">
                        <div class="market-price">{p["price"]}</div>
                        <div class="market-badge">{p["rating"]}</div>
                    </div>
                    <div class="market-seller">by {p["seller"]}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.button(f"Contact Seller", key=f"btn_{i}")

# ═══════════════════════════════════════════════════════
# GOVERNMENT SCHEMES
# ═══════════════════════════════════════════════════════
elif page == "🏛️  Government Schemes":
    st.markdown("""
    <div class="page-title-bar">
        <div class="page-icon-circle">🏛️</div>
        <h1 class="page-title-text">Government Schemes</h1>
    </div>
    <div class="page-subtitle">Discover farmer welfare schemes you are eligible for and apply directly.</div>
    """, unsafe_allow_html=True)

    schemes = [
        {"icon": "💰", "title": "PM-KISAN", "amount": "₹6,000 / year", "desc": "Direct income support transferred to farmer families in three equal instalments.", "who": "All small and marginal farmers", "how": "Apply at pmkisan.gov.in"},
        {"icon": "🌾", "title": "Pradhan Mantri Fasal Bima Yojana", "amount": "Crop Insurance", "desc": "Financial protection against crop loss due to natural calamities, pests and disease.", "who": "All farmers growing notified crops", "how": "Apply through your bank before the sowing season"},
        {"icon": "🏦", "title": "Kisan Credit Card", "amount": "Up to ₹3 Lakh", "desc": "Easy short-term credit at low interest rate for agricultural needs.", "who": "All farmers and sharecroppers", "how": "Apply at any nationalised bank branch"},
        {"icon": "💧", "title": "PM Krishi Sinchai Yojana", "amount": "Irrigation Subsidy", "desc": "Subsidy on micro-irrigation systems like drip and sprinkler to save water.", "who": "All farmers", "how": "Apply at your state agriculture department"},
        {"icon": "🌱", "title": "Soil Health Card Scheme", "amount": "Free Testing", "desc": "Free soil testing every two years with crop-wise nutrient recommendations.", "who": "All farmers across India", "how": "Contact your nearest KVK centre"},
        {"icon": "⚡", "title": "PM KUSUM Yojana", "amount": "90% Solar Subsidy", "desc": "Up to 90% subsidy on solar-powered agricultural irrigation pumps.", "who": "Farmers with agricultural land", "how": "Apply at your state nodal agency"},
    ]

    col1, col2 = st.columns(2)
    for i, s in enumerate(schemes):
        with col1 if i % 2 == 0 else col2:
            st.markdown(f"""
            <div class="scheme-card">
                <div class="scheme-header">
                    <div>
                        <div style="font-size:24px;margin-bottom:4px;">{s["icon"]}</div>
                        <div class="scheme-title">{s["title"]}</div>
                    </div>
                    <div class="scheme-amount">{s["amount"]}</div>
                </div>
                <div class="scheme-desc">{s["desc"]}</div>
                <div class="scheme-detail"><b>Who can apply:</b> {s["who"]}</div>
                <div class="scheme-detail"><b>How to apply:</b> {s["how"]}</div>
            </div>
            """, unsafe_allow_html=True)
            st.button(f"Apply for {s['title']}", key=f"scheme_{i}")

# ═══════════════════════════════════════════════════════
# SMART SURVEY
# ═══════════════════════════════════════════════════════
elif page == "📋  Smart Survey":
    st.markdown("""
    <div class="page-title-bar">
        <div class="page-icon-circle">📋</div>
        <h1 class="page-title-text">Smart Survey</h1>
    </div>
    <div class="page-subtitle">Tell us about your farm and get a personalised step-by-step roadmap.</div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="survey-card">', unsafe_allow_html=True)
    st.markdown('<div style="font-family:\'Playfair Display\',serif;font-size:18px;font-weight:700;color:#1a1008;margin-bottom:18px;">🌾 About Your Farm</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        exp   = st.selectbox("Your farming experience", ["Complete Beginner", "Less than 1 year", "1–3 years", "More than 3 years"])
        land  = st.selectbox("Land available", ["Less than 0.5 acre", "0.5–1 acre", "1–3 acres", "More than 3 acres"])
        water = st.selectbox("Water source", ["Borewell", "Rain-fed only", "Canal / River", "No water source yet"])
    with col2:
        crop  = st.selectbox("Farming interest", ["Vegetables", "Fruits", "Grains / Cereals", "Organic Farming"])
        goal  = st.selectbox("Primary goal", ["Feed my family", "Earn profit", "Sustainable lifestyle", "Learn farming"])
        state = st.selectbox("State", ["Karnataka", "Maharashtra", "Tamil Nadu", "Andhra Pradesh", "Uttar Pradesh", "Other"])

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🌱 Generate My Farm Roadmap"):
        st.markdown("""
        <div style="background:linear-gradient(135deg,#2d6a4f,#40916c);border-radius:20px;padding:24px 28px;margin-bottom:20px;">
            <div style="font-family:'Playfair Display',serif;font-size:22px;font-weight:700;color:#ffffff;">Your Personalised Farm Roadmap</div>
            <div style="font-size:13px;color:rgba(255,255,255,0.75);margin-top:4px;">Based on your inputs — follow these steps for best results.</div>
        </div>
        """, unsafe_allow_html=True)

        if exp == "Complete Beginner":
            steps = [
                ("🧪", "Get your soil tested at the nearest KVK centre — it's free!"),
                ("📐", "Start small — try farming on just 0.25 acre first to learn without big risk."),
                ("🥬", "Grow easy crops like spinach, beans, or ragi to build confidence."),
                ("👥", "Join a local farmer group or WhatsApp community for daily support."),
                ("📋", "Apply for a Soil Health Card through the government's free testing scheme."),
                ("🤖", "Use the AgriConnect AI Assistant daily to answer your farming questions."),
            ]
        else:
            steps = [
                ("🧪", "Re-test your soil for NPK and micro-nutrient levels this season."),
                ("🌱", "Select crops aligned to your land size, water source, and market demand."),
                ("💰", "Apply for PM-KISAN to receive ₹6,000 per year direct support."),
                ("💧", "Install drip irrigation to save up to 50% water and boost yield."),
                ("🏪", "Connect with direct buyers through AgriConnect Marketplace — skip middlemen."),
                ("📡", "Track daily weather and pest alerts using the AgriConnect platform."),
            ]

        for idx, (icon, text) in enumerate(steps):
            st.markdown(f"""
            <div class="step-card" style="display:flex;align-items:center;gap:14px;">
                <div class="step-num">{idx+1}</div>
                <div style="font-size:20px;">{icon}</div>
                <div class="step-text">{text}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        <div style="background:#fdf6ec;border:2px solid #d4a017;border-radius:16px;padding:16px 20px;margin-top:16px;">
            <div style="font-weight:700;color:#3d2b1f;font-size:14px;">💡 Pro Tip</div>
            <div style="font-size:13px;color:#6b5344;margin-top:4px;line-height:1.5;">
                Use the <b>AI Assistant</b> tab to ask daily questions about your crops. The more specific your question, the better the advice!
            </div>
        </div>
        """, unsafe_allow_html=True)