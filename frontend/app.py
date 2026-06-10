import streamlit as st
import requests
from datetime import datetime
import os
import streamlit.components.v1 as components

# --- Page Configuration ---
st.set_page_config(
    page_title="Project SHEild Hub", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- Configuration & High-Contrast Cyber Aesthetics ---
BACKEND_BASE = os.getenv("SHEILD_BACKEND_URL", "http://127.0.0.1:5000")
BACKEND_URL = f"{BACKEND_BASE.rstrip('/')}/analyze"

st.markdown("""
    <style>
    /* 1. High-Saturation Vibrant Quirky Background for Main App */
    .stApp {
        background: linear-gradient(135deg, #1e1b4b 0%, #4c1d95 35%, #701a75 70%, #0369a1 100%) !important;
        background-attachment: fixed !important;
    }
    
    /* 2. Cohesive Diamond Blue Gradient for Sidebar with High Hue/Opacity */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #bbf7d0 0%, #7dd3fc 50%, #38bdf8 100%) !important;
        box-shadow: 5px 0 25px rgba(0, 0, 0, 0.3);
        border-right: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* 3. Force Dark Typography inside Sidebar for Crisp Readability */
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3, 
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] span, 
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] div {
        color: #0f172a !important;
        font-weight: 500 !important;
    }
    
    [data-testid="stSidebar"] div[role="radiogroup"] label {
        background: rgba(255, 255, 255, 0.3);
        padding: 8px 12px;
        border-radius: 10px;
        margin-bottom: 5px;
        transition: all 0.2s ease;
    }
    
    /* 4. Structural Fixes for Native Streamlit Core Containers */
    div[data-testid="stVerticalBlock"] > div:empty,
    div.stVerticalBlock > div[style*="background-color"],
    .stAlert > div {
        display: none !important;
    }
    
    /* 5. Transparent, High-Blur Glassmorphism for Content Cards */
    .custom-card {
        background: rgba(15, 23, 42, 0.45) !important;
        backdrop-filter: blur(20px) saturate(160%);
        -webkit-backdrop-filter: blur(20px) saturate(160%);
        padding: 30px;
        border-radius: 24px;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3);
        margin-bottom: 25px;
        border: 1px solid rgba(255, 255, 255, 0.12);
    }
    
    /* 6. High-Contrast Pure White Typography Overrides */
    .main h1, .main h2, .main h3, .main h4, .main h5, .main h6, 
    .main p, .main span, .main label, .main .stMarkdown,
    [data-testid="stMarkdownContainer"] h1,
    [data-testid="stMarkdownContainer"] h2,
    [data-testid="stMarkdownContainer"] h3,
    [data-testid="stMarkdownContainer"] h4,
    [data-testid="stMarkdownContainer"] p {
        color: #ffffff !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    /* Input field text and placeholder optimization */
    .main textarea::placeholder, .main input::placeholder {
        color: #94a3b8 !important; 
    }
    .main input {
        color: #ffffff !important;
    }
    
    /* 7. Sleek Floating Tech Quote Banner */
    .quote-banner {
        background: rgba(255, 255, 255, 0.07);
        backdrop-filter: blur(10px);
        padding: 24px;
        border-radius: 20px;
        border-left: 6px solid #22d3ee;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    .quote-text {
        font-size: 16px;
        font-style: italic;
        font-weight: 400;
        letter-spacing: 0.3px;
        line-height: 1.5;
        color: #ffffff !important;
    }
    
    /* 8. Interception Panel Styling (Main Content Interface) */
    .interception-panel {
        background: rgba(251, 191, 36, 0.15) !important;
        backdrop-filter: blur(10px);
        padding: 20px;
        border-radius: 16px;
        border-left: 6px solid #f59e0b;
        color: #fffbeb !important;
        margin-top: 15px;
        margin-bottom: 15px;
        border: 1px solid rgba(251, 191, 36, 0.2);
    }

    /* MODAL CONTAINER OVERRIDES */
    div[role="dialog"] {
        background-color: #991b1b !important;
        border: 2px solid #ef4444 !important;
        border-radius: 24px !important;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7) !important;
    }
    div[role="dialog"] button[p-aria-label="Close"] svg, 
    div[role="dialog"] button {
        color: #ffffff !important;
    }
    div[role="dialog"] h1, div[role="dialog"] h2, div[role="dialog"] h3, div[role="dialog"] h4,
    div[role="dialog"] p, div[role="dialog"] span, div[role="dialog"] label, div[role="dialog"] div {
        color: #ffffff !important;
        text-shadow: none !important;
    }
    .modal-intercept-panel {
        background: rgba(0, 0, 0, 0.3) !important;
        padding: 18px;
        border-radius: 14px;
        border-left: 5px solid #ffffff;
        color: #ffffff !important;
        margin-top: 10px;
        margin-bottom: 15px;
    }
    
    /* 9. Feed Post Displays */
    .feed-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        padding: 20px;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        margin-bottom: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    .feed-card div {
        color: #f1f5f9 !important;
    }
    .feed-user {
        color: #22d3ee !important;
        font-weight: 600 !important;
        font-size: 14px;
    }
    
    /* 10. Vibrant Red Custom Post/Login Button Control */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%) !important;
        color: white !important;
        border-radius: 14px !important;
        border: none !important;
        padding: 10px 28px !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 15px rgba(239, 68, 68, 0.4) !important;
        transition: all 0.25s ease-in-out;
    }
    div.stButton > button:first-child:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(239, 68, 68, 0.6) !important;
    }
    
    /* SPECIFIC LIGHTER RED ACTION BUTTON FOR MODAL VIEW */
    div[role="dialog"] div.stButton > button {
        background: linear-gradient(135deg, #f87171 0%, #ef4444 100%) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3) !important;
        font-weight: bold !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    div[role="dialog"] div.stButton > button:hover {
        background: linear-gradient(135deg, #fca5a5 0%, #f87171 100%) !important;
        transform: scale(1.01);
    }
    </style>
""", unsafe_allow_html=True)

# --- Authentication System State Machine ---
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "is_admin" not in st.session_state:
    st.session_state["is_admin"] = False
if "show_warning_modal" not in st.session_state:
    st.session_state["show_warning_modal"] = False
if "harmful_detected" not in st.session_state:
    st.session_state["harmful_detected"] = False
if "scroll_trigger" not in st.session_state:
    st.session_state["scroll_trigger"] = False
if "modal_data" not in st.session_state:
    st.session_state["modal_data"] = {}
# Counter variable used to reset text area buffer cleanly without runtime exceptions
if "textarea_counter" not in st.session_state:
    st.session_state["textarea_counter"] = 0

# --- Render Login Portal First If Not Verified ---
if not st.session_state["authenticated"]:
    left_space, center_login_box, right_space = st.columns([2, 3, 2])
    
    with center_login_box:
        st.markdown("""
            <div class="custom-card" style="margin-top: 15%;">
                <h2 style="margin-top: 0; text-align: center; color: white;">🛡️ Project SHEild Gateway</h2>
                <p style="text-align: center; color: #cbd5e1; margin-bottom: 25px;">Please verify credentials to enter the application portal.</p>
            </div>
        """, unsafe_allow_html=True)
        
        username_input = st.text_input("Username", placeholder="Enter your username...")
        password_input = st.text_input("Password", type="password", placeholder="Enter your password...")
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Authenticate Entry", use_container_width=True):
            if username_input.strip() == "" or password_input.strip() == "":
                st.warning("Please fill out both entry parameters.")
            elif  username_input == "admin" and password_input == "admin":
                st.session_state["authenticated"] = True
                st.session_state["is_admin"] = True
                st.session_state["username"] = username_input
                st.rerun()
            else:
                st.session_state["authenticated"] = True
                st.session_state["is_admin"] = False
                st.session_state["username"] = username_input
                st.rerun()
                
    st.stop()

# --- Sidebar Navigation (Dynamic Access Matrix) ---
st.sidebar.title("🛡️ Project SHEild")
st.sidebar.markdown("---")

navigation_options = ["User Feed & Interface"]
if st.session_state["is_admin"]:
    navigation_options.append("Moderator Console")

page = st.sidebar.radio("Navigation Portal", navigation_options)
st.sidebar.markdown("---")

if st.sidebar.button("Exit Gateway session", use_container_width=True):
    st.session_state["authenticated"] = False
    st.session_state["is_admin"] = False
    st.rerun()

st.sidebar.caption("Hackathon Build v1.2.0 | Security Layer Active")


# --- DIALOG POPUP WARNING UTILITY ---
@st.dialog("⚠️ Policy Enforcement Warning")
def render_harmful_content_modal():
    st.markdown("<h3 style='color: white; margin-top: 0;'>Revise before you post, content is harmful</h3>", unsafe_allow_html=True)
    
    data = st.session_state["modal_data"]
    
    st.markdown(f"""
        <div class="modal-intercept-panel">
            <strong>System Guardrails Active:</strong> Your input string matches signature patterns associated with 
            <strong>{data.get('category')}</strong> domains with <strong>{data.get('severity')}</strong> severity flags.
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("Revise", use_container_width=True):
        st.session_state["show_warning_modal"] = False
        st.session_state["scroll_trigger"] = True
        st.rerun()


# --- Manage Modal Display State Trigger ---
if st.session_state["show_warning_modal"]:
    render_harmful_content_modal()


# ==========================================
# PAGE 1: USER FEED & INTERFACE
# ==========================================
if page == "User Feed & Interface":
    
    st.markdown("""
        <div class="quote-banner">
            <div class="quote-text">
                "Digital spaces achieve true brilliance only when they ensure absolute equality and dignity for every voice."
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="custom-card">
            <h3 style="margin-top: 0; color: white;">Comments Section</h3>
        </div>
    """, unsafe_allow_html=True)
    
    # Text area key parameter utilizes dynamic increment tracking to prevent state exceptions
    current_text_key = f"broadcast_input_{st.session_state['textarea_counter']}"
    user_comment = st.text_area(
        "Input String",
        placeholder="Share your thoughts...", 
        height=120, 
        label_visibility="collapsed",
        key=current_text_key
    )
    
    col_spacer, col_btn = st.columns([10, 2])
    with col_btn:
        submit_triggered = st.button("Post", type="primary", use_container_width=True)

    if submit_triggered:
        if user_comment.strip():
            try:
                response = requests.post(
                BACKEND_URL,
                json={
                    "text": user_comment,
                    "username": st.session_state["username"]
                },
                timeout=5)
                
                if response.status_code == 200:
                    res_data = response.json()
                    warning_triggered = res_data.get("warning", False)
                    
                    st.session_state["modal_data"] = {
                        "score": res_data.get("score", 0),
                        "category": res_data.get("category", "Unknown"),
                        "severity": res_data.get("severity", "Mild")
                    }
                    
                    if warning_triggered:
                        st.session_state["harmful_detected"] = True
                        st.session_state["show_warning_modal"] = True
                        st.rerun()
                    else:
                        st.session_state["harmful_detected"] = False
                        st.success("Analysis confirmed zero threat vectors. Transmission cleared.")
                        st.balloons()
                        st.session_state["textarea_counter"] += 1  # Indirect widget reset
                        st.rerun()
                else:
                    st.error("Infrastructure Interface Error: Invalid network response code recorded.")
            except requests.exceptions.ConnectionError:
                st.error("Backend Disconnect: Verify execution server connectivity state on Port 5000.")
        else:
            st.warning("Input container buffer evaluated as empty. Specify a text parameter.")

    # --- HTML SCROLL TARGET ANCHOR ---
    st.markdown("<div id='analysis-scroll-target'></div>", unsafe_allow_html=True)

    # --- RENDER ANALYSIS METRICS BELOW THE TEXTBOX ONLY ---
    if st.session_state["harmful_detected"]:
        data = st.session_state["modal_data"]
        
        st.markdown(f"""
            <div class="interception-panel">
                <strong>Structural Guardrails Engaged:</strong> System analysis indicates that this string falls under 
                the domain classification of <strong>{data.get('category')}</strong> with <strong>{data.get('severity')}</strong> severity metrics. 
                Modification is advised to adhere to structural platform governance policies.
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### Real-Time Behavioral Signature Analysis")
        m_col1, m_col2, m_col3 = st.columns(3)
        with m_col1:
            st.metric(label="Abuse Vector Weight", value=f"{data.get('score')}%", delta="Boundary Deviation Violation", delta_color="inverse")
        with m_col2:
            st.metric(label="Assigned Domain Class", value=data.get('category'))
        with m_col3:
            st.metric(label="Calculated Urgency Level", value=data.get('severity'))
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # FIXED DETONATION CIRCUIT: Safely increments dynamic keys to flush memory buffer cleanly
        if st.button("Confirm Overwrite & Flag", type="secondary"):
            st.session_state["textarea_counter"] += 1  # Updates widget key context instance
            st.session_state["harmful_detected"] = False  # Collapses verification statistics panel
            st.toast("Submission flagged and input fields cleared.", icon="🛡️")
            st.rerun()

    # --- AUTOMATED JAVASCRIPT SCROLL INTERACTION EXECUTOR ---
    if st.session_state["scroll_trigger"]:
        st.session_state["scroll_trigger"] = False
        components.html(
            """
            <script>
                var element = window.parent.document.getElementById("analysis-scroll-target");
                if (element) {
                    element.scrollIntoView({behavior: "smooth", block: "start"});
                }
            </script>
            """,
            height=0,
            width=0
        )

    st.markdown("### Network Feed Activity")
    st.markdown("""
        <div class="feed-card">
            <div class="feed-user">@engineering_lead</div>
            <div style="margin-top:5px; color:#f1f5f9;">Production compiler optimizations verified. Build sequences are maintaining high algorithmic efficiency bounds.</div>
        </div>
        <div class="feed-card">
            <div class="feed-user">@moderation_node_01</div>
            <div style="margin-top:5px; color:#f1f5f9;">Global threat mitigation layers operating under optimal processing speeds. System logs nominal.</div>
        </div>
    """, unsafe_allow_html=True)

# ==========================================
# PAGE 2: MODERATOR CONSOLE 
# ==========================================
elif page == "Moderator Console" and st.session_state["is_admin"]:
    st.title("System Evaluation & Audit Dashboard")
    st.markdown("Administrative metrics interface tracking automated classification layers.")
    
    stat1, stat2, stat3 = st.columns(3)
    stat1.metric("Pending Verification Logs", "3 Items", delta="Queue Increment Active", delta_color="inverse")
    stat2.metric("Total Mitigation Invocations", "142 Operations")
    
    st.markdown("---")
    st.subheader("Active Verification Stream")
    
    with st.expander("Inspection Object ID: 40912 | Threat Vector: Gender-Based Abuse"):
        st.markdown("**Evaluated Input Payload:** *\"ladkiyan coding nahi kar sakti\"*")
        st.markdown("Analytical Verification Vector: Metric weighting scored structural classification markers at **92%** confidence bounds.")
        
        btn_c1, btn_c2, btn_c3 = st.columns([2, 2, 4])
        with btn_c1:
            if st.button("Discard Alert Object", key="mod_d1"):
                st.success("Evaluation element scrubbed.")
        with btn_c2:
            if st.button("Purge Entry Target", key="mod_p1", type="primary"):
                st.error("Payload deleted globally.")
        with btn_c3:
            if st.button("Escalate to Structural Authorities", key="mod_e1"):
                st.warning("Exporting structural packet details directly to compliance enforcement endpoints.")
