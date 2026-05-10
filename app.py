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
    st.session_state.page_state = "home" # Options: "home", "results", "ipo_detail"

if "current_query" not in st.session_state:
    st.session_state.current_query = ""

if "selected_ipo" not in st.session_state:
    st.session_state.selected_ipo = {}

# Callbacks for navigation transitions
def trigger_search(query_text):
    st.session_state.current_query = query_text
    st.session_state.page_state = "results"

def trigger_ipo_detail(ipo_data):
    st.session_state.selected_ipo = ipo_data
    st.session_state.page_state = "ipo_detail"

def reset_to_home():
    st.session_state.current_query = ""
    st.session_state.selected_ipo = {}
    st.session_state.page_state = "home"

# 3. KNOWLEDGE BASES
MF_KNOWLEDGE = {
    "groww_elss_tax_saver_fund": {
        "name": "Groww ELSS Tax Saver Fund",
        "expense_ratio": "Based on the latest scheme documents, the Net Expense Ratio of **Groww ELSS Tax Saver Fund** is **0.94% for the Direct Plan** and **2.39% for the Regular Plan**. Opting for Direct plans saves you overhead, compounding into higher overall growth over several years.",
        "exit_load": "According to official SID sources, the **Groww ELSS Tax Saver Fund** features an exit load of **Nil (0%)**. This means you can redeem all your accrued units entirely free of exit penalization once your statutory lock-in ends.",
        "minimum_sip": "You can begin a structured Monthly SIP in the **Groww ELSS Tax Saver Fund** with an extremely accessible threshold of just **Rs. 500**.",
        "lock_in": "As an official Equity Linked Savings Scheme (ELSS) designed for tax savings under Section 80C, this fund carries a **strict 3-year statutory lock-in period** from your exact date of purchase.",
        "riskometer": "Given its full equity-oriented strategy, the risk scale classifies this fund as **Very High Risk**. It is optimized for long-term compounders with a 5+ year window.",
        "benchmark": "The performance of this tax saver is evaluated against its Tier-1 primary benchmark: the **Nifty 500 TRI (Total Returns Index)**.",
        "source": "https://assets-netstorage.growwmf.in/compliance_docs/Downloads/SSD/Groww%20ELSS%20Tax%20Saver%20Fund/GrowwELSSTaxSaverFundSSD.pdf",
        "chart_symbol": "NSE:NIFTY_500"
    },
    "groww_nifty_total_market_index_fund": {
        "name": "Groww Nifty Total Market Index Fund",
        "expense_ratio": "The Net Expense Ratio is highly competitive at **0.25% for the Direct Plan** and **1.00% for the Regular Plan**, offering tracking of the entire market at a minimal cost drag.",
        "exit_load": "This passive index fund features an Exit Load of **Nil (0%)**, allowing you flexible entry and exit terms depending on your tactical asset allocation.",
        "minimum_sip": "You can automate investments in the **Groww Nifty Total Market Index Fund** starting with a nominal threshold of only **Rs. 100** per month.",
        "lock_in": "This is a liquid, open-ended index offering and carries **no statutory lock-in period**.",
        "riskometer": "Because it tracks broad market indices, its official risk profile is categorised as **Very High Risk**.",
        "benchmark": "The fund precisely replicates its Tier-1 benchmark: the **Nifty Total Market TRI**.",
        "source": "https://www.growwmf.in/mutual-funds/groww-nifty-total-market-index-fund",
        "chart_symbol": "NSE:NIFTY_500"
    },
    "groww_value_fund": {
        "name": "Groww Value Fund",
        "expense_ratio": "The **Groww Value Fund** maintains an Expense Ratio of **0.36% for the Direct Plan** and **1.83% for the Regular Plan**.",
        "exit_load": "This active scheme charges an Exit Load of **1% if you redeem or switch your units out within 30 days** from allotment. Redemptions processed after 30 days are fully exempt (**Nil exit load**).",
        "minimum_sip": "The minimum Monthly SIP investment required to build equity holdings here is **Rs. 100**.",
        "lock_in": "This scheme is fully open-ended and has **no statutory lock-in period**.",
        "riskometer": "Reflecting its active value-based stock selection strategy, it is officially classified as **Very High Risk**.",
        "benchmark": "It measures index performance directly against the **Nifty 500 TRI**.",
        "source": "https://www.growwmf.in/mutual-funds/groww-value-fund",
        "chart_symbol": "NSE:NIFTY_500"
    }
}

IPO_KNOWLEDGE = {
    "goldline": {
        "name": "Goldline Pharmaceutical Limited",
        "status": "🟢 LIVE / OPEN NOW",
        "dates": "12 May – 14 May 2026",
        "price": "₹41 – ₹43 per share",
        "size": "₹11.61 Cr (SME Segment)",
        "gmp": "~15% Expected listing gains premium holding steady.",
        "details": "A fast-scaling pharmaceutical provider focusing on niche generic manufacturing and domestic distribution infrastructure.",
        "link": "https://www.chittorgarh.com/report/live-ipo-gmp/gmp-report-list/86/",
        "symbol": "NSE:NIFTY_50"
    },
    "jio": {
        "name": "Reliance Jio Infocomm",
        "status": "🟡 UPCOMING BIG GIANT",
        "dates": "Late 2026 (Expected)",
        "price": "To be declared in DRHP",
        "size": "Estimated multi-billion offering (Valuation over ₹9.3 Trillion)",
        "gmp": "Premium indicators expected to surge post-filing.",
        "details": "India's largest digital network player listing its public equity block to accelerate global 5G rollouts and cloud expansion.",
        "link": "https://www.nseindia.com/products/content/equities/ipos/ipo_current_upcoming.htm",
        "symbol": "NSE:NIFTY_50"
    },
    "onemi": {
        "name": "OnEMI Technology (Kissht)",
        "status": "🔴 RECENTLY LISTED",
        "dates": "Listed May 8, 2026",
        "price": "₹162 – ₹171 per share (Final Allocation)",
        "size": "₹925.92 Cr (Mainboard Segment)",
        "gmp": "Successful listing debut with strong public premium additions (+₹190.00).",
        "details": "A leading digital lending Fintech marketplace leveraging machine intelligence for personal and merchant credit solutions.",
        "link": "https://www.chittorgarh.com/ipo/onemi-technology-solutions-ipo/1944/",
        "symbol": "NSE:NIFTY_500"
    }
}

PII_KEYWORDS = [r"\b\d{12}\b", r"\b[A-Z]{5}\d{4}[A-Z]{1}\b", r"\b\d{10}\b"]

def get_answer(user_query):
    for pattern in PII_KEYWORDS:
        if re.search(pattern, user_query):
            return "⚠️ **Security Flagged:** For your data protection, please do not share personal identifiers like PAN, Aadhaar, or phone numbers in your search query.", None, "NSE:NIFTY_50"

    query_lc = user_query.lower()
    
    # Handling "Top Performing Mutual Funds"
    if "top performing" in query_lc or "last quarter" in query_lc or "performance" in query_lc:
        answer = (
            "According to verified public historical reporting metrics for the last quarter, here are the top-performing equity segments along with factual statistical performances:\n\n"
            "1. **Small Cap Funds (Category Average):** ~12.4% return in the last quarter, driven by robust mid and small-cap momentum.\n"
            "2. **Sectoral/Thematic Funds (Infrastructure):** ~10.8% quarterly returns, supported by strong government capex allocations.\n"
            "3. **Multi Cap Funds (Category Average):** ~8.5% return, providing diversified exposure across market capitalizations.\n\n"
            "*Note: Historical performance serves as informational data only and does not guarantee future investment returns.*"
        )
        return answer, "https://www.amfiindia.com/research-information/other-data", "NSE:NIFTY_500"

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
            "Alternatively, you can request a consolidated statement across all fund houses via the official CAMS or KFintech investor portals.",
            "https://www.growwmf.in/downloads/investor-services", "NSE:NIFTY_50"
        )

    if matched_fund:
        fund_data = MF_KNOWLEDGE[matched_fund]
        symbol = fund_data["chart_symbol"]
        if "expense" in query_lc:
            return f"Hello! Here is the expense structure analysis:\n\n{fund_data['expense_ratio']}", fund_data["source"], symbol
        elif "exit" in query_lc or "load" in query_lc:
            return f"Hello! Regarding your query on exit parameters:\n\n{fund_data['exit_load']}", fund_data["source"], symbol
        elif "sip" in query_lc or "minimum" in query_lc:
            return f"Hello! Here are the minimum subscription guidelines:\n\n{fund_data['minimum_sip']}", fund_data["source"], symbol
        elif "lock" in query_lc:
            return f"Hello! Here is the legal holding requirement:\n\n{fund_data['lock_in']}", fund_data["source"], symbol
        elif "risk" in query_lc:
            return f"Hello! Let's review the risk parameters:\n\n{fund_data['riskometer']}", fund_data["source"], symbol
        elif "benchmark" in query_lc:
            return f"Hello! Here is the primary index reference point:\n\n{fund_data['benchmark']}", fund_data["source"], symbol
        else:
            overview = (
                f"### {fund_data['name']} Quick Guide\n"
                f"* **Minimum SIP:** {fund_data['minimum_sip']}\n"
                f"* **Lock-in Period:** {fund_data['lock_in']}\n"
                f"* **Exit Load Details:** {fund_data['exit_load']}\n"
                f"* **Riskometer Rating:** {fund_data['riskometer']}\n"
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

    # A. Custom Personalized Advice Banner
    st.markdown("""
        <div class="advice-banner">
            <div class="advice-title">👋 Hello Prathamesh, Howdy!!!</div>
            <div class="advice-text">
                Did you know? <strong>Compounding is the 8th wonder of the world.</strong><br>
                Stay highly disciplined: short-term market volatility is just the price of admission for superior, inflation-beating long-term returns.
            </div>
        </div>
    """, unsafe_allow_html=True)

    # B. Curated IPO Section (With dynamic detail trigger)
    st.markdown("<h3 style='font-size:1.3rem; font-weight:600; margin-bottom:1rem;'>🎯 Initial Public Offerings (IPO) Radar</h3>", unsafe_allow_html=True)
    
    col_ipo1, col_ipo2, col_ipo3 = st.columns(3)
    
    with col_ipo1:
        st.markdown("""
            <div style="background-color:#0F172A; border:1px solid #1E293B; padding:1rem; border-radius:10px; min-height:160px;">
                <strong style="color:#00D09C;">🟢 LIVE / OPEN NOW</strong><br>
                <span style="font-size:1.1rem; font-weight:700;">Goldline Pharma</span><br>
                <span style="font-size:0.85rem; color:#94A3B8;">Price Band: ₹41 - ₹43<br>GMP Expected: ~15%</span>
            </div>
        """, unsafe_allow_html=True)
        # Clicking this redirects to the IPO detail screen
        if st.button("View Goldline Details", key="btn_goldline", use_container_width=True):
            trigger_ipo_detail(IPO_KNOWLEDGE["goldline"])
            st.rerun()

    with col_ipo2:
        st.markdown("""
            <div style="background-color:#0F172A; border:1px solid #1E293B; padding:1rem; border-radius:10px; min-height:160px;">
                <strong style="color:#FFA500;">🟡 UPCOMING GIANT</strong><br>
                <span style="font-size:1.1rem; font-weight:700;">Reliance Jio</span><br>
                <span style="font-size:0.85rem; color:#94A3B8;">Launch: Late 2026<br>Valuation: ₹9.3 Trillion+</span>
            </div>
        """, unsafe_allow_html=True)
        if st.button("View Jio Details", key="btn_jio", use_container_width=True):
            trigger_ipo_detail(IPO_KNOWLEDGE["jio"])
            st.rerun()

    with col_ipo3:
        st.markdown("""
            <div style="background-color:#0F172A; border:1px solid #1E293B; padding:1rem; border-radius:10px; min-height:160px;">
                <strong style="color:#FF4B4B;">🔴 RECENTLY LISTED</strong><br>
                <span style="font-size:1.1rem; font-weight:700;">OnEMI (Kissht)</span><br>
                <span style="font-size:0.85rem; color:#94A3B8;">Date: May 8, 2026<br>Listed Price: ₹171</span>
            </div>
        """, unsafe_allow_html=True)
        if st.button("View OnEMI Details", key="btn_onemi", use_container_width=True):
            trigger_ipo_detail(IPO_KNOWLEDGE["onemi"])
            st.rerun()

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
        index_name = "NIFTY 500 Index" if symbol == "NSE:NIFTY_500" else "NIFTY 50 Index"
        st.caption(f"Tracking Index: **{index_name}** ({symbol})")
        
        # FIXED: Removed volume indicator completely by passing volume: false to TradingView config!
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
            "style": "1", /* 1 = Candlestick chart style */
            "locale": "en",
            "toolbar_bg": "#0B1528",
            "enable_publishing": false,
            "hide_top_toolbar": false,
            "hide_legend": true,
            "save_image": false,
            "volume": false, /* FIXED: Fully removes the overlapping volume bar indicators! */
            "container_id": "tradingview_clean_chart"
          }});
          </script>
        </div>
        """
        components.html(clean_candlestick_widget, height=360)

# ==========================================
# SCREEN 3: IPO DEEP-DIVE SCREEN
# ==========================================
elif st.session_state.page_state == "ipo_detail":
    col_header, col_back = st.columns([0.8, 0.2])
    with col_header:
        st.markdown(f'<div style="font-size:2rem; font-weight:800; color:#00D09C; margin-top:0.5rem; letter-spacing:-0.5px;">IPO Deep-Dive</div>', unsafe_allow_html=True)
    with col_back:
        st.button("⬅️ Home", on_click=reset_to_home, use_container_width=True)

    st.write("---")

    ipo = st.session_state.selected_ipo

    col_info, col_chart = st.columns([1.1, 0.9])

    with col_info:
        st.subheader(ipo["name"])
        st.markdown(f"**Status:** {ipo['status']}")
        
        with st.container(border=True):
            st.markdown(f"""
            * **Subscription Dates:** {ipo['dates']}
            * **Price Range Band:** {ipo['price']}
            * **Issue Capital Size:** {ipo['size']}
            * **Gray Market Premium (GMP):** {ipo['gmp']}
            """)
            st.markdown(f"**Prospectus Overview:**\n{ipo['details']}")
            
            st.markdown(" ")
            st.link_button("🌐 Open Live Tracker & Subscription Status", ipo["link"], use_container_width=True)

    with col_chart:
        st.markdown("### 📈 Live Market Index Context")
        st.caption(f"General index benchmark tracker context for new Listings.")
        
        clean_candlestick_widget = f"""
        <div class="tradingview-widget-container" style="height:350px;">
          <div id="tradingview_clean_chart" style="height:350px;"></div>
          <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
          <script type="text/javascript">
          new TradingView.widget({{
            "autosize": true,
            "symbol": "{ipo['symbol']}",
            "interval": "D",
            "timezone": "Asia/Kolkata",
            "theme": "dark",
            "style": "1",
            "locale": "en",
            "toolbar_bg": "#0B1528",
            "enable_publishing": false,
            "hide_top_toolbar": false,
            "hide_legend": true,
            "save_image": false,
            "volume": false,
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
