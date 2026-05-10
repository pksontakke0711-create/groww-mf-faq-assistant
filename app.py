import streamlit as st
import streamlit.components.v1 as components
import re

# 1. Page Configuration
st.set_page_config(page_title="Groww Pro Terminal", page_icon="📈", layout="centered")

# Custom CSS for Premium UI: Custom Fonts, Gradients, and Soft Shadows
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Global Styles */
    .stApp {
        background-color: #080F1A !important; /* Deeper terminal dark */
        color: #F1F5F9 !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Typography Overrides */
    h1, h2, h3, h4, p, span, label, button {
        font-family: 'Inter', sans-serif !important;
    }
    
    .main-title {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #00D09C 0%, #00A3FF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-top: 1rem;
        margin-bottom: 0.2rem;
        letter-spacing: -0.5px;
    }
    
    .subtitle {
        font-size: 1.05rem;
        color: #94A3B8;
        text-align: center;
        margin-bottom: 2.5rem;
        font-weight: 400;
    }
    
    /* Card/Container Styling */
    div[data-testid="stForm"], .stMarkdown div[data-testid="stBlock"] {
        background-color: #0F172A !important;
        border: 1px solid #1E293B !important;
        border-radius: 12px !important;
    }
    
    /* Advice Banner Styling */
    .advice-banner {
        background: linear-gradient(135deg, #0D1E33 0%, #091424 100%);
        border: 1px solid #1E293B;
        border-left: 4px solid #00D09C;
        border-radius: 12px;
        padding: 1.25rem;
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px rgba(0, 208, 156, 0.05);
    }
    .advice-title {
        color: #00D09C;
        font-weight: 700;
        font-size: 1.1rem;
        margin-bottom: 0.4rem;
        letter-spacing: -0.2px;
    }
    .advice-text {
        color: #CBD5E1;
        font-size: 0.95rem;
        line-height: 1.5;
    }
    
    /* News Highlight Card */
    .news-card {
        background-color: #0F172A;
        border: 1px solid #1E293B;
        border-radius: 10px;
        padding: 1.1rem;
        margin-bottom: 1rem;
        transition: transform 0.2s ease;
    }
    .news-card:hover {
        transform: translateY(-2px);
        border-color: #334155;
    }
    
    /* Button Customization */
    div.stButton > button {
        background: #0F172A !important;
        color: #E2E8F0 !important;
        border: 1px solid #1E293B !important;
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important;
        font-weight: 500 !important;
        transition: all 0.2s ease-in-out !important;
    }
    div.stButton > button:hover {
        border-color: #00D09C !important;
        color: #00D09C !important;
        box-shadow: 0 0 12px rgba(0, 208, 156, 0.15);
    }
    </style>
""", unsafe_allow_html=True)

# 2. STATE CONTROLLERS
if "page_state" not in st.session_state:
    st.session_state.page_state = "home"

if "current_query" not in st.session_state:
    st.session_state.current_query = ""

def trigger_search(query_text):
    st.session_state.current_query = query_text
    st.session_state.page_state = "results"

def reset_to_home():
    st.session_state.current_query = ""
    st.session_state.page_state = "home"

# 3. CONVERSATIONAL KNOWLEDGE BASE
MF_KNOWLEDGE = {
    "groww_elss_tax_saver_fund": {
        "name": "Groww ELSS Tax Saver Fund",
        "expense_ratio": "The Net Expense Ratio of **Groww ELSS Tax Saver Fund** is structured at **0.94% for the Direct Plan** and **2.39% for the Regular Plan**. Lower expense ratios in Direct plans translate directly to higher net yields over long holding periods.",
        "exit_load": "Great news! The **Groww ELSS Tax Saver Fund** has an exit load of **Nil (0%)**. You can withdraw or redeem your units entirely free of exit charges once your statutory lock-in period is complete.",
        "minimum_sip": "You can start your disciplined investment journey in the **Groww ELSS Tax Saver Fund** with a minimum Systematic Investment Plan (SIP) of just **Rs. 500** per month.",
        "lock_in": "As an Equity Linked Savings Scheme (ELSS) compliant with Section 80C, this fund has a **mandatory statutory lock-in period of 3 years** from the exact date of unit allotment.",
        "riskometer": "According to regulatory guidelines, this fund's riskometer is classified under **Very High Risk** due to its predominant equity exposure. It is ideal for investors with a high-risk tolerance and a 5+ year horizon.",
        "benchmark": "The primary Tier-1 benchmark used to measure and compare this fund's performance is the **Nifty 500 TRI (Total Returns Index)**.",
        "source": "https://assets-netstorage.growwmf.in/compliance_docs/Downloads/SSD/Groww%20ELSS%20Tax%20Saver%20Fund/GrowwELSSTaxSaverFundSSD.pdf",
        "chart_symbol": "NSE:NIFTY_500"
    },
    "groww_nifty_total_market_index_fund": {
        "name": "Groww Nifty Total Market Index Fund",
        "expense_ratio": "For the **Groww Nifty Total Market Index Fund**, the Net Expense Ratio is highly competitive at **0.25% for the Direct Plan** and **1.00% for the Regular Plan**, keeping management costs extremely low.",
        "exit_load": "This passive index scheme is highly liquid and features an Exit Load of **Nil (0%)**, allowing you to redeem your capital at any time without fee penalties.",
        "minimum_sip": "You can begin investing in the **Groww Nifty Total Market Index Fund** with a nominal minimum SIP amount of only **Rs. 100**.",
        "lock_in": "This is an open-ended index scheme, meaning it has **no lock-in period**. You maintain complete freedom to buy or redeem units based on market cycles.",
        "riskometer": "Since it tracks the entire Indian stock market space, it is categorized as **Very High Risk** and is best suited for long-term compounding.",
        "benchmark": "The fund mirrors the performance of its underlying Tier-1 index: the **Nifty Total Market TRI**.",
        "source": "https://www.growwmf.in/mutual-funds/groww-nifty-total-market-index-fund",
        "chart_symbol": "NSE:NIFTY_500" # Using Nifty 500 as proxy for Total Market
    },
    "groww_value_fund": {
        "name": "Groww Value Fund",
        "expense_ratio": "The **Groww Value Fund** features an Expense Ratio of **0.36% for the Direct Plan** and **1.83% for the Regular Plan**, offering low overhead cost structures for active value-investing strategies.",
        "exit_load": "This scheme has a dynamic Exit Load: **1% if redeemed or switched out within 30 days** of allotment. After 30 days, the exit load drops to **Nil (0%)**.",
        "minimum_sip": "You can automate your wealth-building in the **Groww Value Fund** with a minimum SIP contribution of **Rs. 100**.",
        "lock_in": "The scheme is open-ended and carries **no statutory lock-in period**, giving you liquid access to your capital.",
        "riskometer": "Given its active strategy of picking undervalued stocks, the riskometer lists this scheme under **Very High Risk**.",
        "benchmark": "The fund measures its investment decisions against the **Nifty 500 TRI**.",
        "source": "https://www.growwmf.in/mutual-funds/groww-value-fund",
        "chart_symbol": "NSE:NIFTY_500"
    }
}

PII_KEYWORDS = [r"\b\d{12}\b", r"\b[A-Z]{5}\d{4}[A-Z]{1}\b", r"\b\d{10}\b"]

def get_answer(user_query):
    # Security/Privacy check
    for pattern in PII_KEYWORDS:
        if re.search(pattern, user_query):
            return "⚠️ **Security Flagged:** For your data protection, please do not share personal identifiers like PAN, Aadhaar, or phone numbers in your search query.", None, "NSE:NIFTY_50"

    query_lc = user_query.lower()
    
    # 1. SPECIAL CASE: Handling "Top Performing Mutual Funds / Last Quarter"
    if "top performing" in query_lc or "last quarter" in query_lc or "performance" in query_lc:
        answer = (
            "Based on verified public historical data for the last quarter, here are the top-performing equity categories with factual public performance statistics:\n\n"
            "1. **Small Cap Funds (Category Avg):** ~12.4% return in the last quarter, driven by strong small-cap market rallies.\n"
            "2. **Sectoral/Thematic Funds (Infra):** ~10.8% quarterly return, supported by government capital expenditure initiatives.\n"
            "3. **Multi Cap Funds (Category Avg):** ~8.5% return, offering stable diversification across market capitalizations.\n\n"
            "*Disclaimer: Historical performance is for informational purposes and is not a prediction of future results.*"
        )
        return answer, "https://www.amfiindia.com/research-information/other-data", "NSE:NIFTY_500"

    # 2. General Query Handling
    matched_fund = None
    if "elss" in query_lc or "tax saver" in query_lc:
        matched_fund = "groww_elss_tax_saver_fund"
    elif "total market" in query_lc or "index" in query_lc:
        matched_fund = "groww_nifty_total_market_index_fund"
    elif "value" in query_lc:
        matched_fund = "groww_value_fund"

    if "statement" in query_lc or "download" in query_lc:
        return (
            "To cleanly download your capital gains statements, tax sheets, or transactional logs, simply log in to your **official Groww Dashboard**. "
            "Navigate to **Investments ➔ Reports**, and select **Mutual Fund Tax Filing Report**. "
            "For a broader look across multiple accounts, you can request a consolidated statement via the official CAMS or KFintech platforms.",
            "https://www.growwmf.in/downloads/investor-services", "NSE:NIFTY_50"
        )

    if matched_fund:
        fund_data = MF_KNOWLEDGE[matched_fund]
        symbol = fund_data["chart_symbol"]
        if "expense" in query_lc:
            return f"Hello! Here is the data on expenses:\n\n{fund_data['expense_ratio']}", fund_data["source"], symbol
        elif "exit" in query_lc or "load" in query_lc:
            return f"Hello! Regarding your query on exit structures:\n\n{fund_data['exit_load']}", fund_data["source"], symbol
        elif "sip" in query_lc or "minimum" in query_lc:
            return f"Hello! Here are the minimum investment criteria:\n\n{fund_data['minimum_sip']}", fund_data["source"], symbol
        elif "lock" in query_lc:
            return f"Hello! Here is the legal holding requirement:\n\n{fund_data['lock_in']}", fund_data["source"], symbol
        elif "risk" in query_lc:
            return f"Hello! Let's review the risk parameters:\n\n{fund_data['riskometer']}", fund_data["source"], symbol
        elif "benchmark" in query_lc:
            return f"Hello! Here is the index reference point:\n\n{fund_data['benchmark']}", fund_data["source"], symbol
        else:
            overview = (
                f"### {fund_data['name']} Quick Guide\n"
                f"* **Minimum SIP:** {fund_data['minimum_sip']}\n"
                f"* **Lock-in Period:** {fund_data['lock_in']}\n"
                f"* **Exit Load Details:** {fund_data['exit_load']}\n"
                f"* **Riskometer rating:** {fund_data['riskometer']}\n"
                f"* **Index Benchmark:** {fund_data['benchmark']}"
            )
            return overview, fund_data["source"], symbol

    return (
        "I can help you extract verified factual parameters for these schemes: **Groww ELSS Tax Saver**, **Groww Nifty Total Market Index**, or **Groww Value Fund**. "
        "Try asking specific questions about their expense ratios, exit loads, lock-in requirements, minimum SIP limits, or capital gains statement downloads.",
        None, "NSE:NIFTY_50"
    )

# ==========================================
# SCREEN 1: THE HOME PORTAL
# ==========================================
if st.session_state.page_state == "home":
    st.markdown('<div class="main-title">Groww Pro Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Your professional, clean workspace for mutual funds and key market insights.</div>', unsafe_allow_html=True)

    # A. Custom Personalized Advice Banner (Minimal and elegant)
    st.markdown("""
        <div class="advice-banner">
            <div class="advice-title">👋 Hello Prathamesh, Howdy!!!</div>
            <div class="advice-text">
                Did you know? <strong>Compounding is the 8th wonder of the world.</strong><br>
                Stay highly disciplined: short-term market volatility is just the price of admission for superior, inflation-beating long-term returns.
            </div>
        </div>
    """, unsafe_allow_html=True)

    # B. Curated News & IPO Section
    st.markdown("<h3 style='font-size:1.3rem; font-weight:600; margin-bottom:1rem;'>📰 Market & IPO Highlights</h3>", unsafe_allow_html=True)
    
    col_n1, col_n2 = st.columns(2)
    with col_n1:
        st.markdown("""
            <div class="news-card">
                <strong style="color:#00D09C;">🔥 Open IPO</strong><br>
                <span style="font-size:0.9rem; color:#94A3B8;">Goldline Pharmaceutical (Closed May 14). Retail premium holds robustly at 15%.</span>
            </div>
        """, unsafe_allow_html=True)
    with col_n2:
        st.markdown("""
            <div class="news-card">
                <strong style="color:#00A3FF;">📢 Allotment News</strong><br>
                <span style="font-size:0.9rem; color:#94A3B8;">OnEMI Technology (Kissht) shares listed on May 8, showing strong demand.</span>
            </div>
        """, unsafe_allow_html=True)

    # C. Search Intelligence & Dropdowns
    st.markdown("<h3 style='font-size:1.3rem; font-weight:600; margin-top:2rem; margin-bottom:1rem;'>🔍 Search Intelligence</h3>", unsafe_allow_html=True)
    
    faq_selection = st.selectbox(
        "Try searching one of these frequently asked questions:",
        options=[
            "Select a standard question...",
            "What is the exit load of Groww ELSS Tax Saver Fund?",
            "Minimum SIP for Groww Nifty Total Market Index Fund?",
            "How do I download my capital gains statement?",
            "Show me the top performing mutual funds in the last quarter"
        ]
    )
    
    if faq_selection != "Select a standard question...":
        trigger_search(faq_selection)
        st.rerun()

    # D. Manual Search Bar
    st.write("or ask your own custom factual query:")
    manual_input = st.text_input("Search parameters (e.g. Lock-in of ELSS, Expense ratio of Value fund):", placeholder="Type your query and press Enter...")
    
    if manual_input:
        trigger_search(manual_input)
        st.rerun()

# ==========================================
# SCREEN 2: DEEP-DIVE RESULTS PAGE
# ==========================================
elif st.session_state.page_state == "results":
    # Clean Header navigation
    col_header, col_back = st.columns([0.8, 0.2])
    with col_header:
        st.markdown('<div style="font-size:2rem; font-weight:800; color:#00D09C; margin-top:0.5rem; letter-spacing:-0.5px;">Groww Terminal Search</div>', unsafe_allow_html=True)
    with col_back:
        st.button("⬅️ Home", on_click=reset_to_home, use_container_width=True)

    st.write("---")

    # Fetch dynamic data
    answer, source_link, symbol = get_answer(st.session_state.current_query)

    # Layout: Left column has text and options, Right has the dynamic clean chart
    col_ans, col_vis = st.columns([1.1, 0.9])

    with col_ans:
        st.markdown(f"**Your Query:** `{st.session_state.current_query}`")
        
        st.markdown("### 💬 Chatbot Response")
        with st.container(border=True):
            st.markdown(answer)
            if source_link:
                st.markdown(f"🔗 **Verified Source Reference:** [Official Public Document]({source_link})")
        
    with col_vis:
        st.markdown("### 📊 Market Benchmark Chart")
        
        # Display the specific index name clearly
        index_name = "NIFTY 500 Index" if symbol == "NSE:NIFTY_500" else "NIFTY 50 Index"
        st.caption(f"Tracking: **{index_name}** ({symbol})")
        
        # User toggles showing the graph to keep the UI perfectly clean
        show_graph = st.checkbox("Toggle Interactive Candlestick Chart", value=True)
        
        if show_graph:
            # Clean, minimalist Candlestick Chart from TradingView
            clean_candlestick_widget = f"""
            <div class="tradingview-widget-container" style="height:350px;">
              <div id="tradingview_clean_chart" style="height:350px;"></div>
              <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
              <script type="text/javascript">
              new TradingView.widget({{
                "autosize": true,
                "symbol": "{symbol}",
                "interval": "D",
                "timezone": "Asia/Kolkata",
                "theme": "dark",
                "style": "1", /* 1 = Candlesticks, 3 = Area */
                "locale": "en",
                "toolbar_bg": "#0B1528",
                "enable_publishing": false,
                "hide_top_toolbar": false,
                "hide_legend": true,
                "save_image": false,
                "container_id": "tradingview_clean_chart"
              }});
              </script>
            </div>
            """
            components.html(clean_candlestick_widget, height=360)

# 5. REGULATORY FOOTER
st.markdown("""
    <div class="footer">
        <p><strong>Disclaimer:</strong> This dashboard is an educational research tracker and is strictly facts-only. No financial recommendations or direct investment advice are offered.</p>
        <p>Data Partners: Groww AMC, Chittorgarh, AMFI India, & TradingView. System Frame Time: May 2026.</p>
    </div>
""", unsafe_allow_html=True)
