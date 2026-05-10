import streamlit as st
import streamlit.components.v1 as components
import re

# 1. Page Configuration (Set to Dark Mode Style natively)
st.set_page_config(page_title="Groww Pro Terminal", page_icon="📈", layout="centered")

# Custom CSS for the Deep Navy & Groww Green Theme
st.markdown("""
    <style>
    /* Main Background & Text Color Defaults */
    .stApp {
        background-color: #0B1528 !important;
        color: #F8F9FA !important;
    }
    .main-title {
        font-size: 2.6rem;
        font-weight: 800;
        color: #00D09C; /* Groww Green */
        text-align: center;
        margin-top: 1rem;
        margin-bottom: 0.2rem;
    }
    .subtitle {
        font-size: 1.1rem;
        color: #8A99AD;
        text-align: center;
        margin-bottom: 2rem;
    }
    /* Advice Banner Styling */
    .advice-banner {
        background: linear-gradient(135deg, #0f2b46, #07192b);
        border: 1px solid #00D09C;
        border-radius: 12px;
        padding: 1.2rem;
        margin-bottom: 2rem;
    }
    .advice-title {
        color: #00D09C;
        font-weight: 700;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
    }
    .advice-text {
        color: #E2E8F0;
        font-size: 0.95rem;
        line-height: 1.4;
    }
    /* News Section Container */
    .news-container {
        background-color: #12223C;
        border: 1px solid #1E3A64;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 2rem;
    }
    /* Footer Styling */
    .footer {
        margin-top: 5rem;
        padding-top: 1.5rem;
        border-top: 1px solid #1E3A64;
        color: #64748B;
        font-size: 0.8rem;
        text-align: center;
    }
    /* Override standard button UI to match dark navy theme */
    div.stButton > button {
        background-color: #12223C !important;
        color: #F8F9FA !important;
        border: 1px solid #1E3A64 !important;
        border-radius: 6px !important;
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        border-color: #00D09C !important;
        color: #00D09C !important;
        transform: translateY(-1px);
    }
    </style>
""", unsafe_allow_html=True)

# 2. STATE CONTROLLERS
# Setup state keys to manage transitions between Screen 1 and Screen 2
if "page_state" not in st.session_state:
    st.session_state.page_state = "home" # Options: "home" or "results"

if "current_query" not in st.session_state:
    st.session_state.current_query = ""

# Callback function when a user submits or clicks an FAQ
def trigger_search(query_text):
    st.session_state.current_query = query_text
    st.session_state.page_state = "results"

def reset_to_home():
    st.session_state.current_query = ""
    st.session_state.page_state = "home"

# 3. KNOWLEDGE DATABASES
MF_KNOWLEDGE = {
    "groww_elss_tax_saver_fund": {
        "name": "Groww ELSS Tax Saver Fund",
        "expense_ratio": "The Net Expense Ratio is 0.94% for the Direct Plan and 2.39% for the Regular Plan.",
        "exit_load": "This scheme has an Exit Load of Nil (0%).",
        "minimum_sip": "The minimum application amount for a Systematic Investment Plan (SIP) is Rs. 500.",
        "lock_in": "As an Equity Linked Savings Scheme (ELSS), this fund has a statutory lock-in period of 3 years from the date of allotment.",
        "riskometer": "The product riskometer is categorized as Very High Risk.",
        "benchmark": "The Tier-1 benchmark for this scheme is Nifty 500 TRI.",
        "source": "https://assets-netstorage.growwmf.in/compliance_docs/Downloads/SSD/Groww%20ELSS%20Tax%20Saver%20Fund/GrowwELSSTaxSaverFundSSD.pdf"
    },
    "groww_nifty_total_market_index_fund": {
        "name": "Groww Nifty Total Market Index Fund",
        "expense_ratio": "The Net Expense Ratio is 0.25% for the Direct Plan and 1.00% for the Regular Plan.",
        "exit_load": "This scheme has an Exit Load of Nil (0%).",
        "minimum_sip": "The minimum application amount for a Systematic Investment Plan (SIP) is Rs. 100.",
        "lock_in": "There is no lock-in period for this open-ended index scheme.",
        "riskometer": "The product riskometer is categorized as Very High Risk.",
        "benchmark": "The Tier-1 benchmark for this scheme is Nifty Total Market TRI.",
        "source": "https://www.growwmf.in/mutual-funds/groww-nifty-total-market-index-fund"
    },
    "groww_value_fund": {
        "name": "Groww Value Fund",
        "expense_ratio": "The Net Expense Ratio is 0.36% for the Direct Plan and 1.83% for the Regular Plan.",
        "exit_load": "The exit load is 1% if units are redeemed or switched out within 30 days from the date of allotment, and Nil thereafter.",
        "minimum_sip": "The minimum application amount for a Systematic Investment Plan (SIP) is Rs. 100.",
        "lock_in": "There is no lock-in period for this open-ended equity scheme.",
        "riskometer": "The product riskometer is categorized as Very High Risk.",
        "benchmark": "The Tier-1 benchmark for this scheme is Nifty 500 TRI.",
        "source": "https://www.growwmf.in/mutual-funds/groww-value-fund"
    },
    "statements": {
        "download": "To download your capital gains statement, account statement, or tax documents, log into the official Groww web or mobile dashboard, navigate to 'Investments' -> 'Reports', and select 'Mutual Fund Tax Filing Report'. Alternatively, you can request a consolidated account statement (CAS) via the CAS official platforms using your registered email.",
        "source": "https://www.growwmf.in/downloads/investor-services"
    }
}

PII_KEYWORDS = [r"\b\d{12}\b", r"\b[A-Z]{5}\d{4}[A-Z]{1}\b", r"\b\d{10}\b", r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"]
ADVICE_KEYWORDS = ["should i buy", "should i sell", "which is best", "is it good", "is it safe", "how much return", "predict", "guarantee", "recommend", "top performing", "best fund", "last year", "returns"]

def scan_for_pii(query):
    for pattern in PII_KEYWORDS:
        if re.search(pattern, query): return True
    return False

def check_for_advice(query):
    return any(kw in query.lower() for kw in ADVICE_KEYWORDS)

def get_answer(user_query):
    if scan_for_pii(user_query):
        return "⚠️ **ERROR:** For security and privacy, please do not share personal identifiers like PAN or Aadhaar. Query blocked.", None

    if check_for_advice(user_query):
        return ("❌ **Investment Advice Restricted:** I cannot recommend funds, predict performance, or rank schemes. "
                "For educational resources on evaluating mutual funds, please visit the Association of Mutual Funds in India (AMFI):", 
                "https://www.amfiindia.com/investor-corner")

    query_lc = user_query.lower()
    matched_fund = None
    
    if "elss" in query_lc or "tax saver" in query_lc:
        matched_fund = "groww_elss_tax_saver_fund"
    elif "total market" in query_lc or "index" in query_lc:
        matched_fund = "groww_nifty_total_market_index_fund"
    elif "value" in query_lc:
        matched_fund = "groww_value_fund"

    if "statement" in query_lc or "download" in query_lc:
        return MF_KNOWLEDGE["statements"]["download"], MF_KNOWLEDGE["statements"]["source"]

    if matched_fund:
        fund_data = MF_KNOWLEDGE[matched_fund]
        if "expense" in query_lc:
            return fund_data["expense_ratio"], fund_data["source"]
        elif "exit" in query_lc or "load" in query_lc:
            return fund_data["exit_load"], fund_data["source"]
        elif "sip" in query_lc or "minimum" in query_lc:
            return fund_data["minimum_sip"], fund_data["source"]
        elif "lock" in query_lc:
            return fund_data["lock_in"], fund_data["source"]
        elif "risk" in query_lc:
            return fund_data["riskometer"], fund_data["source"]
        elif "benchmark" in query_lc:
            return fund_data["benchmark"], fund_data["source"]
        else:
            return f"**{fund_data['name']} Overview:**\n- **Minimum SIP:** {fund_data['minimum_sip']}\n- **Exit Load:** {fund_data['exit_load']}\n- **Risk Profile:** {fund_data['riskometer']}\n- **Benchmark:** {fund_data['benchmark']}", fund_data["source"]

    return ("I can only answer specific factual queries regarding **Groww ELSS Tax Saver**, **Groww Nifty Total Market Index**, and **Groww Value Fund**. "
            "Please try asking about their expense ratios, exit loads, lock-ins, minimum SIP amounts, or how to download statements."), None

# ==========================================
# SCREEN 1: THE PORTAL HOME PAGE
# ==========================================
if st.session_state.page_state == "home":
    st.markdown('<div class="main-title">Groww Pro Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Your private, verified terminal for Mutual Funds and market indexes.</div>', unsafe_allow_html=True)

    # A. Custom Interactive Advice Banner (Shortened & Personalized)
    st.markdown("""
        <div class="advice-banner">
            <div class="advice-title">👋 Hello Prathamesh, Howdy!!!</div>
            <div class="advice-text">
                Do you know? Compounding is the 8th wonder of the world. 
                Keep discipline: volatility is simply the entry fee for premium, long-term market returns.
            </div>
        </div>
    """, unsafe_allow_html=True)

    # B. Dynamic News & IPO Section 
    st.markdown("### 📰 Market & IPO Highlights")
    with st.container(border=True):
        col_n1, col_n2 = st.columns(2)
        with col_n1:
            st.markdown("""
            **🔥 Open SME IPO:** * **Goldline Pharmaceutical** (Closed May 14, 2026). Expected listing gains around ~15%.
            """)
        with col_n2:
            st.markdown("""
            **📢 Mainboard Allotments:** * **OnEMI Technology (Kissht)** listed robustly on May 8, 2026 with strong retail subscriptions.
            """)

    # C. Frequently Asked Questions Dropdown
    st.markdown("### 🔍 Search Intelligence")
    faq_selection = st.selectbox(
        "Try searching one of these frequently asked questions:",
        options=[
            "Select a standard question...",
            "What is the exit load of Groww ELSS Tax Saver Fund?",
            "Minimum SIP for Groww Nifty Total Market Index Fund?",
            "How do I download my capital gains statement?"
        ]
    )
    
    if faq_selection != "Select a standard question...":
        trigger_search(faq_selection)
        st.rerun()

    # D. Custom Search Input Box
    st.write("or ask your own specific parameter query:")
    manual_input = st.text_input("Search parameter details (e.g. Lock-in period of ELSS, Expense ratio of Value fund):", placeholder="Type your question here and press enter...")
    
    if manual_input:
        trigger_search(manual_input)
        st.rerun()

# ==========================================
# SCREEN 2: DEEP-DIVE RESULTS SCREEN
# ==========================================
elif st.session_state.page_state == "results":
    # Header area with an easy-to-use "Back to Home" button
    col_header, col_back = st.columns([0.8, 0.2])
    with col_header:
        st.markdown('<div style="font-size:2rem; font-weight:800; color:#00D09C; margin-top:0.5rem;">Groww Terminal Search</div>', unsafe_allow_html=True)
    with col_back:
        st.button("⬅️ Go Back", on_click=reset_to_home, use_container_width=True)

    st.write("---")

    # Double Column Layout: Left (Answers/Sources) & Right (Theme-Matched Live Index Chart)
    col_ans, col_vis = st.columns([1.1, 0.9])

    with col_ans:
        st.markdown(f"**Your Query:** `{st.session_state.current_query}`")
        
        st.markdown("### 💬 Chatbot Response")
        with st.container(border=True):
            answer, source_link = get_answer(st.session_state.current_query)
            st.markdown(answer)
            if source_link:
                st.markdown(f"🔗 **Verified Source Reference:** [Official Public Document]({source_link})")

    with col_vis:
        st.markdown("### 📈 Real-Time Index Support")
        st.caption("Review live market benchmarks dynamically to support your query context.")
        
        # Theme-Matched Dark TradingView Widget
        dark_tradingview_widget = """
        <div class="tradingview-widget-container" style="height:350px;">
          <div id="tradingview_dark_nifty" style="height:350px;"></div>
          <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
          <script type="text/javascript">
          new TradingView.widget({
            "autosize": true,
            "symbol": "NSE:NIFTY_500",
            "interval": "D",
            "timezone": "Asia/Kolkata",
            "theme": "dark",
            "style": "3",
            "locale": "en",
            "toolbar_bg": "#12223C",
            "enable_publishing": false,
            "hide_top_toolbar": false,
            "hide_legend": true,
            "save_image": false,
            "container_id": "tradingview_dark_nifty"
          });
          </script>
        </div>
        """
        components.html(dark_tradingview_widget, height=360)

# 5. REGULATORY FOOTER (Renders consistently at the base of both screens)
st.markdown("""
    <div class="footer">
        <p><strong>Disclaimer:</strong> This dashboard is an educational research tracker and is strictly facts-only. No financial recommendations, returns evaluations, or direct investment advice are offered.</p>
        <p>Data Partners: Groww AMC, Chittorgarh, AMFI India, & TradingView. System Frame Time: May 2026.</p>
    </div>
""", unsafe_allow_html=True)
