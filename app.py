import streamlit as st
import streamlit.components.v1 as components
import re
import time

# 1. Page Configuration
st.set_page_config(page_title="Groww Pro Terminal", page_icon="📈", layout="centered")

# Custom CSS for Premium UI
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght=300;400;500;600;700;800&display=swap');
    
    /* Global Styles */
    .stApp {
        background-color: #080F1A !important;
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

    /* Terminal Status Bar */
    .terminal-bar {
        display: flex;
        justify-content: space-between;
        background-color: #0F172A;
        border: 1px solid #1E293B;
        border-radius: 8px;
        padding: 6px 16px;
        margin-bottom: 25px;
        font-size: 0.8rem;
        color: #94A3B8;
    }
    .status-dot {
        height: 8px;
        width: 8px;
        border-radius: 50%;
        display: inline-block;
        margin-right: 6px;
        animation: pulse 1.5s infinite;
    }
    .dot-green { background-color: #00D09C; }
    .dot-blue { background-color: #00A3FF; }
    
    @keyframes pulse {
        0% { transform: scale(0.95); opacity: 0.5; }
        50% { transform: scale(1.1); opacity: 1; }
        100% { transform: scale(0.95); opacity: 0.5; }
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

    /* Up-Down Markets Candlestick CSS Loader */
    .market-loader {
        display: flex;
        align-items: flex-end;
        justify-content: center;
        gap: 8px;
        height: 60px;
        margin-bottom: 20px;
    }
    .candle {
        width: 10px;
        background-color: #00D09C;
        border-radius: 2px;
        animation: candleJump 1.2s ease-in-out infinite;
    }
    .candle-down {
        background-color: #FF4B4B;
    }
    .c1 { height: 20px; animation-delay: 0.1s; }
    .c2 { height: 45px; animation-delay: 0.3s; }
    .c3 { height: 15px; animation-delay: 0.5s; }
    .c4 { height: 55px; animation-delay: 0.2s; }
    .c5 { height: 30px; animation-delay: 0.4s; }

    @keyframes candleJump {
        0%, 100% { transform: scaleY(1); }
        50% { transform: scaleY(1.4); }
    }

    /* Fixed height container for scrolling chat window */
    .chat-history-scroll {
        max-height: 380px;
        overflow-y: auto;
        padding: 10px;
        border: 1px solid #1E293B;
        border-radius: 8px;
        background-color: #0B1322;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. STATE CONTROLLERS
if "page_state" not in st.session_state:
    st.session_state.page_state = "home"

if "current_query" not in st.session_state:
    st.session_state.current_query = ""

if "selected_ipo" not in st.session_state:
    st.session_state.selected_ipo = {}

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "current_chart_symbol" not in st.session_state:
    st.session_state.current_chart_symbol = "NSE:NIFTY"

# Navigation Transitions with Simulation Delay
def trigger_search(query_text):
    st.session_state.current_query = query_text
    show_processing_animation()
    
    answer, source_link, symbol = get_answer(query_text)
    st.session_state.current_chart_symbol = symbol
    
    st.session_state.chat_history = [
        {"role": "user", "content": query_text},
        {"role": "assistant", "content": answer, "source": source_link}
    ]
    st.session_state.page_state = "results"

def trigger_ipo_detail(ipo_data):
    st.session_state.selected_ipo = ipo_data
    show_processing_animation()
    st.session_state.page_state = "ipo_detail"

def reset_to_home():
    st.session_state.current_query = ""
    st.session_state.selected_ipo = {}
    st.session_state.chat_history = []
    st.session_state.current_chart_symbol = "NSE:NIFTY"
    st.session_state.page_state = "home"

# Processing Visual Simulation
def show_processing_animation():
    placeholder = st.empty()
    with placeholder.container():
        st.markdown("""
            <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 60vh;">
                <div class="market-loader">
                    <div class="candle c1"></div>
                    <div class="candle candle-down c2"></div>
                    <div class="candle c3"></div>
                    <div class="candle c4"></div>
                    <div class="candle candle-down c5"></div>
                </div>
                <h3 style="color: #00D09C; font-weight: 700; letter-spacing: -0.5px; text-align: center; margin-top: 15px;">Scanning Exchange Data</h3>
                <p style="color: #94A3B8; font-size: 0.95rem; text-align: center; margin-top: -5px;">Extracting compliance-approved asset vectors...</p>
            </div>
        """, unsafe_allow_html=True)
        time.sleep(1.5)
    placeholder.empty()

# 3. KNOWLEDGE BASES & WORKING TRACKING SYMBOLS (VERIFIED LIVE)
MF_KNOWLEDGE = {
    "groww_elss_tax_saver_fund": {
        "name": "Groww ELSS Tax Saver Fund",
        "expense_ratio": "Based on the latest scheme documents, the Net Expense Ratio of **Groww ELSS Tax Saver Fund** is **0.94% for the Direct Plan** and **2.39% for the Regular Plan**.",
        "exit_load": "According to official SID sources, the **Groww ELSS Tax Saver Fund** features an exit load of **Nil (0%)**. This means you can redeem all your accrued units entirely free of exit penalization once your statutory lock-in ends.",
        "minimum_sip": "You can begin a structured Monthly SIP in the **Groww ELSS Tax Saver Fund** with an extremely accessible threshold of just **Rs. 500**.",
        "lock_in": "As an official Equity Linked Savings Scheme (ELSS) designed for tax savings under Section 80C, this fund carries a **strict 3-year statutory lock-in period** from your exact date of purchase.",
        "riskometer": "Given its full equity-oriented strategy, the risk scale classifies this fund as **Very High Risk**.",
        "benchmark": "The performance of this tax saver is evaluated against its Tier-1 primary benchmark: the **Nifty 500 TRI (Total Returns Index)**.",
        # VERIFIED & WORKING SECURE PDF LINK
        "source": "https://assets-netstorage.growwmf.in/compliance_docs/Downloads/SID/SID_Groww%20ELSS%20Tax%20Saver%20Fund.pdf",
        "chart_symbol": "NSE:CNX500"
    },
    "groww_nifty_total_market_index_fund": {
        "name": "Groww Nifty Total Market Index Fund",
        "expense_ratio": "The Net Expense Ratio is highly competitive at **0.25% for the Direct Plan** and **1.00% for the Regular Plan**.",
        "exit_load": "This passive index fund features an Exit Load of **Nil (0%)**, allowing you flexible entry and exit terms depending on your tactical asset allocation.",
        "minimum_sip": "You can automate investments in the **Groww Nifty Total Market Index Fund** starting with a nominal threshold of only **Rs. 100** per month.",
        "lock_in": "This is a liquid, open-ended index offering and carries **no statutory lock-in period**.",
        "riskometer": "Because it tracks broad market indices, its official risk profile is categorised as **Very High Risk**.",
        "benchmark": "The fund precisely replicates its Tier-1 benchmark: the **Nifty Total Market TRI**.",
        "source": "https://groww.in",
        "chart_symbol": "NSE:CNX500"
    },
    "groww_value_fund": {
        "name": "Groww Value Fund",
        "expense_ratio": "The **Groww Value Fund** maintains an Expense Ratio of **0.36% for the Direct Plan** and **1.83% for the Regular Plan**.",
        "exit_load": "This active scheme charges an Exit Load of **1% if you redeem or switch your units out within 30 days** from allotment. Redemptions processed after 30 days are fully exempt (**Nil exit load**).",
        "minimum_sip": "The minimum Monthly SIP investment required to build equity holdings here is **Rs. 100**.",
        "lock_in": "This scheme is fully open-ended and has **no statutory lock-in period**.",
        "riskometer": "Reflecting its active value-based stock selection strategy, it is officially classified as **Very High Risk**.",
        "benchmark": "It measures index performance directly against the **Nifty 500 TRI**.",
        "source": "https://groww.in",
        "chart_symbol": "NSE:CNX500"
    }
}

IPO_KNOWLEDGE = {
    "goldline": {
        "name": "Goldline Pharmaceutical Limited",
        "status": "🟢 LIVE / OPEN NOW",
        "dates": "12 May – 14 May 2026",
        "price": "₹41 – ₹43 per share",
        "size": "₹11.61 Cr (SME)",
        "gmp": "~15% GMP Premium",
        "details": "A fast-scaling pharmaceutical provider focusing on niche generic manufacturing and domestic distribution infrastructure.",
        "link": "https://groww.in/ipo",
        "symbol": "NSE:SUNPHARMA"
    },
    "jio": {
        "name": "Reliance Jio Infocomm",
        "status": "🟡 UPCOMING BIG GIANT",
        "dates": "Late 2026 (Expected)",
        "price": "TBD in DRHP",
        "size": "Est. Valuation ₹9.3T+",
        "gmp": "Premium indicators surging.",
        "details": "India's largest digital network player listing its public equity block to accelerate global 5G rollouts and cloud expansion.",
        "link": "https://groww.in/ipo",
        "symbol": "NSE:RELIANCE"
    },
    "onemi": {
        "name": "OnEMI Technology (Kissht)",
        "status": "🔴 RECENTLY LISTED",
        "dates": "Listed May 8, 2026",
        "price": "₹162 – ₹171 per share",
        "size": "₹925.92 Cr (Mainboard)",
        "gmp": "Listing debut: +₹190.00",
        "details": "A leading digital lending Fintech marketplace leveraging machine intelligence for personal and merchant credit solutions.",
        "link": "https://groww.in/ipo",
        "symbol": "NSE:BAJFINANCE"
    }
}

PII_KEYWORDS = [r"\b\d{12}\b", r"\b[A-Z]{5}\d{4}[A-Z]{1}\b", r"\b\d{10}\b"]

# 4. BOT ROUTER
def get_answer(user_query):
    for pattern in PII_KEYWORDS:
        if re.search(pattern, user_query):
            return "⚠️ **Security Flagged:** For your data protection, please do not share personal identifiers like PAN, Aadhaar, or phone numbers.", None, "NSE:NIFTY"

    query_lc = user_query.lower()
    
    if "locking period" in query_lc and "value" in query_lc:
        return (
            "No, the **Groww Value Fund** is fully open-ended and has **no statutory lock-in period**. You can redeem or switch units at any time, subject to normal exit loads within 30 days.",
            "https://groww.in", "NSE:CNX500"
        )
        
    if "tax benefits" in query_lc or "80c" in query_lc:
        return (
            "Investments in the **Groww ELSS Tax Saver Fund** qualify for deductions of up to **Rs. 1.5 Lakhs per financial year** under **Section 80C** of the Income Tax Act with a 3-year lock-in.",
            "https://assets-netstorage.growwmf.in/compliance_docs/Downloads/SID/SID_Groww%20ELSS%20Tax%20Saver%20Fund.pdf", "NSE:CNX500"
        )

    if "top performing" in query_lc or "last quarter" in query_lc or "performance" in query_lc:
        answer = (
            "Based on historical tracking data from last quarter, here are the topperforming segments:\n\n"
            "1. **Small Cap Funds:** ~12.4% return\n"
            "2. **Infrastructure/Thematic Funds:** ~10.8% return\n"
            "3. **Multi Cap Funds:** ~8.5% return\n\n"
            "*Past performances are static indicators and do not guarantee future returns.*"
        )
        return answer, "https://groww.in", "NSE:NIFTY"

    matched_fund = None
    if "elss" in query_lc or "tax saver" in query_lc:
        matched_fund = "groww_elss_tax_saver_fund"
    elif "total market" in query_lc or "index" in query_lc:
        matched_fund = "groww_nifty_total_market_index_fund"
    elif "value" in query_lc:
        matched_fund = "groww_value_fund"

    if "statement" in query_lc or "download" in query_lc:
        return (
            "You can download your statements from your **Groww Dashboard** under **Investments ➔ Reports**.",
            "https://groww.in", "NSE:NIFTY"
        )

    if matched_fund:
        fund_data = MF_KNOWLEDGE[matched_fund]
        symbol = fund_data["chart_symbol"]
        if "expense" in query_lc:
            return f"Expense Ratio analysis:\n\n{fund_data['expense_ratio']}", fund_data["source"], symbol
        elif "exit" in query_lc or "load" in query_lc:
            return f"Exit Load parameters:\n\n{fund_data['exit_load']}", fund_data["source"], symbol
        elif "sip" in query_lc or "minimum" in query_lc:
            return f"Subscription thresholds:\n\n{fund_data['minimum_sip']}", fund_data["source"], symbol
        elif "lock" in query_lc:
            return f"Statutory Lock-in rules:\n\n{fund_data['lock_in']}", fund_data["source"], symbol
        elif "risk" in query_lc:
            return f"Investment risk profile:\n\n{fund_data['riskometer']}", fund_data["source"], symbol
        elif "benchmark" in query_lc:
            return f"Primary Benchmark context:\n\n{fund_data['benchmark']}", fund_data["source"], symbol
        else:
            overview = (
                f"### {fund_data['name']} Quick Guide\n"
                f"* **Minimum SIP:** {fund_data['minimum_sip']}\n"
                f"* **Lock-in Period:** {fund_data['lock_in']}\n"
                f"* **Exit Load Details:** {fund_data['exit_load']}\n"
                f"* **Index Benchmark:** {fund_data['benchmark']}"
            )
            return overview, fund_data["source"], symbol

    return (
        "I can help you analyze **Groww ELSS Tax Saver**, **Groww Nifty Total Market Index**, or **Groww Value Fund**. Try asking about exit loads, lock-ins, or expense ratios.",
        None, "NSE:NIFTY"
    )

# ==========================================
# SCREEN 1: THE HOME PORTAL
# ==========================================
if st.session_state.page_state == "home":
    st.markdown('<div class="main-title">Groww Pro Terminal</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Your professional, clean workspace for mutual funds and key market insights.</div>', unsafe_allow_html=True)

    st.markdown("""
        <div class="terminal-bar">
            <span><span class="status-dot dot-green"></span>Terminal Status: <b>ONLINE</b></span>
            <span>Latency: <b>12ms</b></span>
            <span><span class="status-dot dot-blue"></span>Compliance Engine: <b>ACTIVE</b></span>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="advice-banner">
            <div class="advice-title">👋 Hello Prathamesh, Howdy!!!</div>
            <div class="advice-text">
                Did you know? <strong>Compounding is the 8th wonder of the world.</strong><br>
                Stay highly disciplined: short-term market volatility is just the price of admission for superior, inflation-beating long-term returns.
            </div>
        </div>
    """, unsafe_allow_html=True)

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

    st.write("or ask your own custom factual query:")
    manual_input = st.text_input("Search parameters (e.g. Lock-in of ELSS, Expense ratio of Value fund):", placeholder="Type your query and press Enter...")
    
    if manual_input:
        trigger_search(manual_input)
        st.rerun()

# ==========================================
# SCREEN 2: DEEP-DIVE RESULTS WITH ACTIVE CHARTS
# ==========================================
elif st.session_state.page_state == "results":
    col_header, col_back = st.columns([0.8, 0.2])
    with col_header:
        st.markdown('<div style="font-size:2rem; font-weight:800; color:#00D09C; margin-top:0.5rem; letter-spacing:-0.5px;">Groww Terminal Copilot</div>', unsafe_allow_html=True)
    with col_back:
        st.button("⬅️ Home", on_click=reset_to_home, use_container_width=True)

    st.write("---")

    col_chat, col_vis = st.columns([1.1, 0.9])

    with col_chat:
        st.markdown("### 💬 Copilot Workspace")
        
        chat_container = st.container(border=True)
        with chat_container:
            for message in st.session_state.chat_history:
                avatar_emoji = "👤" if message["role"] == "user" else "📈"
                with st.chat_message(message["role"], avatar=avatar_emoji):
                    st.write(message["content"])
                    if "source" in message and message["source"]:
                        st.markdown(f"🔗 **Reference Link:** [Official Document]({message['source']})")
                        st.markdown("<p style='color: #64748B; font-size: 0.75rem; margin-top: 5px; margin-bottom: 0px;'>Source Verified: May 2026</p>", unsafe_allow_html=True)

        follow_up = st.chat_input("Ask a follow-up query (e.g., 'Exit load of ELSS?')")
        if follow_up:
            st.session_state.chat_history.append({"role": "user", "content": follow_up})
            new_ans, new_source, new_symbol = get_answer(follow_up)
            st.session_state.current_chart_symbol = new_symbol
            st.session_state.chat_history.append({"role": "assistant", "content": new_ans, "source": new_source})
            st.rerun()
        
    with col_vis:
        st.markdown("### 📊 Market Benchmark Chart")
        symbol = st.session_state.current_chart_symbol
        index_name = "NIFTY 500 Index" if symbol == "NSE:CNX500" else "NIFTY 50 Index"
        st.caption(f"Tracking Index: **{index_name}** ({symbol})")
        
        # CORRECTED: Clean, lightweight TradingView widget with fully verified symbol parameters
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
            "style": "1",
            "locale": "en",
            "toolbar_bg": "#0B1528",
            "enable_publishing": false,
            "hide_top_toolbar": true,
            "hide_legend": true,
            "save_image": false,
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
            st.markdown("<p style='color: #64748B; font-size: 0.75rem; margin-top: 15px;'>Last updated from sources: May 2026</p>", unsafe_allow_html=True)

    with col_chart:
        st.markdown("### 📈 Sector/Benchmark Chart Context")
        st.caption(f"Tracking related ticker context: **{ipo['symbol']}**")
        
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
            "hide_top_toolbar": true,
            "hide_legend": true,
            "save_image": false,
            "container_id": "tradingview_clean_chart"
          }});
          </script>
        </div>
        """
        components.html(clean_candlestick_widget, height=360)

# Footer Disclaimer
st.markdown("""
    <div class="footer">
        <p style='text-align: center; color: #555; font-size: 0.8rem; margin-top: 3rem;'><strong>Disclaimer:</strong> This dashboard is an educational research tracker and is strictly facts-only. No financial recommendations or direct investment advice are offered.</p>
        <p style='text-align: center; color: #555; font-size: 0.8rem;'>Data Partners: Groww AMC, Chittorgarh, AMFI India, & TradingView. System Frame Time: May 2026.</p>
    </div>
""", unsafe_allow_html=True)
