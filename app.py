import streamlit as st
import re

# Page Config & Header
st.set_page_config(page_title="Groww MF FAQ Assistant", page_icon="📈", layout="centered")
st.title("📈 Groww Mutual Fund FAQ Assistant")
st.caption("Last updated from sources: May 2026")
st.warning("⚠️ **Disclaimer:** Facts-only. No investment advice. Personal identifiers (like PAN, Aadhaar, or account numbers) are strictly prohibited.")

# Knowledge Base
KNOWLEDGE_BASE = {
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

# Security Check Functions
PII_KEYWORDS = [r"\b\d{12}\b", r"\b[A-Z]{5}\d{4}[A-Z]{1}\b", r"\b\d{10}\b", r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"]
ADVICE_KEYWORDS = ["should i buy", "should i sell", "which is best", "is it good", "is it safe", "how much return", "predict", "guarantee", "recommend"]

def scan_for_pii(query):
    for pattern in PII_KEYWORDS:
        if re.search(pattern, query): return True
    return False

def check_for_advice(query):
    return any(kw in query.lower() for kw in ADVICE_KEYWORDS)

def get_answer(user_query):
    if scan_for_pii(user_query):
        return "⚠️ **ERROR:** For security and privacy, please do not share personal information like PAN, Aadhaar, phone numbers, or account details. This query has been blocked.", None

    if check_for_advice(user_query):
        return ("I cannot provide financial advice, recommendations, or performance forecasts. "
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
        return KNOWLEDGE_BASE["statements"]["download"], KNOWLEDGE_BASE["statements"]["source"]

    if matched_fund:
        fund_data = KNOWLEDGE_BASE[matched_fund]
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
            return f"{fund_data['name']} has a minimum SIP of {fund_data['minimum_sip']} and an exit load of {fund_data['exit_load']}.", fund_data["source"]

    return "I can only answer specific factual questions about Groww ELSS Tax Saver, Nifty Total Market Index, or Value Fund. Please ask about expense ratios, exit loads, lock-ins, minimum SIPs, or statement downloads.", None

# UI Elements
st.markdown("### 💡 Example Questions to Try:")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Exit load of ELSS Fund?"):
        st.session_state.query_input = "What is the exit load of Groww ELSS Tax Saver Fund?"
with col2:
    if st.button("Minimum SIP for Index?"):
        st.session_state.query_input = "Minimum SIP for Groww Nifty Total Market Index Fund?"
with col3:
    if st.button("How to download statement?"):
        st.session_state.query_input = "How do I download my capital gains statement?"

user_query = st.text_input("Ask a factual question about Groww mutual funds:", key="query_input")

if user_query:
    answer, source_link = get_answer(user_query)
    st.markdown("#### **Answer:**")
    st.write(answer)
    if source_link:
        st.markdown(f"🔗 **Source Reference:** [Official Public Document]({source_link})")
