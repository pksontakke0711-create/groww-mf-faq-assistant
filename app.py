import streamlit as st
import streamlit.components.v1 as components
import re

# 1. Page Configuration (Title, Icon, Layout)
st.set_page_config(page_title="Groww Pro Dashboard", page_icon="📈", layout="wide")

# Custom CSS styling for a modern Groww Brand (Dark/Light Balance)
st.markdown("""
    <style>
    .main-title {
        font-size: 2.8rem;
        font-weight: 800;
        color: #00D09C; /* Groww Green */
        text-align: center;
        margin-top: -1rem;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        font-size: 1.15rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .footer {
        margin-top: 5rem;
        padding-top: 1.5rem;
        border-top: 1px solid #eee;
        color: #888;
        font-size: 0.85rem;
        text-align: center;
    }
    div[data-testid="stExpander"] {
        background-color: #F8F9FA;
        border: 1px solid #EAEAEA;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. POP-UP DIALOG (The Wealth Compounding Mindset Pop-up)
# This function defines what shows inside the Welcome Modal
@st.dialog("🌱 Your Wealth Journey Begins Here")
def welcome_modal():
    st.markdown("### Compounding is the 8th Wonder of the world!")
    st.markdown("""
    Investing ₹5,000 every month for 15 years doesn't just grow your savings—it secures your absolute freedom. 
    Before entering your analytical dashboard, keep these fundamental principles in mind:
    """)
    
    col_pro, col_con = st.columns(2)
    with col_pro:
        st.success("""
        **Pros of Long-Term SIPs:**
        * **Rupee Cost Averaging:** You buy more when markets are low, and less when they are high.
        * **Power of Compounding:** Your earnings earn earnings!
        """)
    with col_con:
        st.error("""
        **The Reality (Cons):**
        * **Volatility:** Markets go up and down. Short-term drops are normal.
        * **Patience Required:** Real wealth takes a minimum of 5–7 years to truly accelerate.
        """)
        
    st.info("⚠️ **Disclaimer:** Factual tools only. No direct investment advice. Volatility is the price of admission for inflation-beating returns.")
    
    # FIXED PARAMETER HERE: Changed use_container_type to use_container_width
    if st.button("Enter Dashboard 🚀", type="primary", use_container_width=True):
        st.session_state.popup_dismissed = True
        st.rerun()

# Check short term memory (session state) to see if we need to launch the pop-up
if "popup_dismissed" not in st.session_state:
    st.session_state.popup_dismissed = False

if not st.session_state.popup_dismissed:
    welcome_modal()

# 3. KNOWLEDGE BASES
# Facts on mutual funds from official Groww documents
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
        "download": "To download your capital gains statement, account statement, or tax documents, log into the official Groww web or mobile dashboard, navigate to 'Investments' -> 'Reports', and select 'Mutual Fund Tax Filing Report'. Alternatively, you can request a consolidated account statement (CAS) via the KFintech or CAMS official platforms using your registered email.",
        "source": "https://www.growwmf.in/downloads/investor-services"
    }
}

PII_KEYWORDS = [r"\b\d{12}\b", r"\b[A-Z]{5}\d{4}[A-Z]{1}\b", r"\b\d{10}\b", r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"]
ADVICE_KEYWORDS = ["should i buy", "should i sell", "which is best", "is it good", "is it safe", "how much return", "predict", "guarantee", "recommend", "top performing", "best fund", "last year", "returns"]

# Security functions
def scan_for_pii(query):
    for pattern in PII_KEYWORDS:
        if re.search(pattern, query): return True
    return False

def check_for_advice(query):
    return any(kw in query.lower() for kw in ADVICE_KEYWORDS)

def get_answer(user_query):
    if scan_for_pii(user_query):
        return "⚠️ **ERROR:** For security, please do not enter personal indicators (like PAN, Aadhaar, account numbers, or personal phone numbers). This query was auto-blocked.", None

    if check_for_advice(user_query):
        return ("❌ **Investment Advice Restricted:** I cannot provide financial recommendations or performance comparisons. "
                "For verified resources on assessing mutual fund performance, please consult the Association of Mutual Funds in India (AMFI):", 
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

# 4. APP DESIGN LAYOUT (Header section)
st.markdown('<div class="main-title">Groww Pro Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Your private, verified terminal for Mutual Funds and live IPO tracking.</div>', unsafe_allow_html=True)

# Navigation Tabs
tab_mf, tab_ipo = st.tabs(["📊 Mutual Fund Assistant", "🚀 IPO Tracker"])

# --- TAB 1: MUTUAL FUND CO-PILOT ---
with tab_mf:
    col_input, col_chart = st.columns([1.1, 0.9])
    
    with col_input:
        st.markdown("### 💬 Ask the Assistant")
        
        # Session State Setup for quick questions
        if "search_query" not in st.session_state:
            st.session_state.search_query = ""
            
        def set_query(query_text):
            st.session_state.search_query = query_text
            
        # Quick-click FAQ buttons
        st.caption("Frequently Asked:")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.button("Exit load of ELSS?", on_click=set_query, args=("What is the exit load of Groww ELSS Tax Saver Fund?",))
        with c2:
            st.button("Index Fund Min SIP?", on_click=set_query, args=("Minimum SIP for Groww Nifty Total Market Index Fund?",))
        with c3:
            st.button("Get My Statements?", on_click=set_query, args=("How do I download my capital gains statement?",))
            
        # Interactive Search Bar
        user_query = st.text_input("Enter your factual question about Groww mutual funds here:", value=st.session_state.search_query, key="mf_search_bar")
        
        if user_query:
            st.markdown("#### **Answer Card:**")
            with st.container(border=True):
                answer, source_link = get_answer(user_query)
                st.markdown(answer)
                if source_link:
                    st.markdown(f"🔗 **Verified Source Reference:** [Official Public Document]({source_link})")
                    
    with col_chart:
        st.markdown("### 📈 Live Market Benchmark Chart")
        st.caption("Tracking the **NIFTY 500 Index** (Primary Benchmark for Indian Equities)")
        
        # Real-time Interactive TradingView Widget
        # This renders a fully-functional JS chart block right inside our clean page!
        tradingview_widget = """
        <div class="tradingview-widget-container" style="height:350px;">
          <div id="tradingview_nifty500" style="height:350px;"></div>
          <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
          <script type="text/javascript">
          new TradingView.widget({
            "autosize": true,
            "symbol": "NSE:NIFTY_500",
            "interval": "D",
            "timezone": "Asia/Kolkata",
            "theme": "light",
            "style": "3",
            "locale": "en",
            "toolbar_bg": "#f1f3f6",
            "enable_publishing": false,
            "hide_top_toolbar": false,
            "hide_legend": true,
            "save_image": false,
            "container_id": "tradingview_nifty500"
          });
          </script>
        </div>
        """
        components.html(tradingview_widget, height=360)

# --- TAB 2: LIVE IPO TRACKER ---
with tab_ipo:
    st.markdown("### 🎯 Initial Public Offerings (IPO) Radar")
    st.markdown("Monitor upcoming opportunities, live subscriptions, and listed premiums cleanly.")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<h4 style="color:#00D09C;">🟢 LIVE / OPEN NOW</h4>', unsafe_allow_html=True)
        with st.container(border=True):
            st.subheader("Goldline Pharmaceutical")
            st.markdown("""
            - **Subscription Period:** 12 May – 14 May 2026
            - **Price Band:** ₹41 – ₹43 per share
            - **Issue Size:** ₹11.61 Cr (SME)
            - **Live GMP Status:** ~15% Premium Expected
            """)
            st.link_button("View Live GMP Tracker", "https://www.chittorgarh.com/report/live-ipo-gmp/gmp-report-list/86/")

    with col2:
        st.markdown('<h4 style="color:#FFA500;">🟡 UPCOMING GIANT</h4>', unsafe_allow_html=True)
        with st.container(border=True):
            st.subheader("Reliance Jio Infocomm")
            st.markdown("""
            - **Expected Launch:** Late 2026
            - **Estimated Valuation:** Over ₹9.3 Trillion
            - **Issue Size:** Giant Multi-Billion Offer
            - **Focus:** Digital expansion & 5G infrastructure
            """)
            st.link_button("View DRHP Updates", "https://www.nseindia.com/products/content/equities/ipos/ipo_current_upcoming.htm")

    with col3:
        st.markdown('<h4 style="color:#FF4B4B;">🔴 RECENTLY LISTED</h4>', unsafe_allow_html=True)
        with st.container(border=True):
            st.subheader("OnEMI Technology (Kissht)")
            st.markdown("""
            - **Listing Date:** May 8, 2026
            - **Issue Price:** ₹162 – ₹171 per share
            - **Total Issue Size:** ₹925.92 Cr (Mainboard)
            - **Final Listing Performance:** Opened with solid premiums (+₹190.00).
            """)
            st.link_button("View Allotment & Financials", "https://www.chittorgarh.com/ipo/onemi-technology-solutions-ipo/1944/")

# 5. REGULATORY FOOTER (Clean and at the bottom)
st.markdown("""
    <div class="footer">
        <p><strong>Disclaimer:</strong> This dashboard is an educational research tracker and is strictly facts-only. No financial suggestions or investment advice are offered. Stock and index values are streamed via third-party providers and should be verified independently.</p>
        <p>Data Partners: Groww Public Factsheets, Chittorgarh, AMFI India, & TradingView Developer Tools. Current System Time: May 2026.</p>
    </div>
""", unsafe_allow_html=True)
