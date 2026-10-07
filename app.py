import os
import time
from pathlib import Path

import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from google import genai


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="BizAI | Business Support System",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"
DOCUMENTS_DIR = BASE_DIR / "documents"


# ============================================================
# ENVIRONMENT / API KEY
# ============================================================

load_dotenv(BASE_DIR / ".env")

try:
    GEMINI_API_KEY = st.secrets.get(
        "GEMINI_API_KEY",
        os.getenv("GEMINI_API_KEY")
    )
except Exception:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


# ============================================================
# PREMIUM DARK GREEN DESIGN
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       GLOBAL
    ======================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 15% 15%,
                rgba(34, 197, 94, 0.08),
                transparent 25%
            ),
            radial-gradient(
                circle at 85% 20%,
                rgba(16, 185, 129, 0.07),
                transparent 25%
            ),
            #050807;

        color: #f8fafc;
    }


    .main .block-container {
        max-width: 1450px;
        padding-top: 1.5rem;
        padding-bottom: 4rem;
    }


    header[data-testid="stHeader"] {
        background: transparent;
    }


    /* ========================================================
       BUTTONS
    ======================================================== */

    .stButton > button {

        min-height: 48px;

        border-radius: 12px;

        background:
            linear-gradient(
                135deg,
                #16a34a,
                #22c55e
            );

        border: 1px solid rgba(134, 239, 172, 0.3);

        color: white;

        font-weight: 800;

        box-shadow:
            0 8px 30px rgba(34, 197, 94, 0.15);

        transition: all 0.2s ease;
    }


    .stButton > button:hover {

        transform: translateY(-2px);

        background:
            linear-gradient(
                135deg,
                #22c55e,
                #4ade80
            );

        box-shadow:
            0 12px 40px rgba(34, 197, 94, 0.25);
    }


    /* ========================================================
       METRICS
    ======================================================== */

    [data-testid="stMetric"] {

        background:
            linear-gradient(
                145deg,
                rgba(15, 25, 19, 0.95),
                rgba(8, 15, 11, 0.95)
            );

        border:
            1px solid
            rgba(34, 197, 94, 0.13);

        border-radius: 18px;

        padding: 22px;

        box-shadow:
            0 15px 40px rgba(0, 0, 0, 0.20);
    }


    [data-testid="stMetricLabel"] {
        color: #64748b !important;
    }


    [data-testid="stMetricValue"] {
        color: #f8fafc !important;
    }


    /* ========================================================
       INPUT
    ======================================================== */

    .stTextInput > div > div > input {

        background: #0b120d !important;

        color: white !important;

        border:
            1px solid
            rgba(34, 197, 94, 0.18) !important;

        border-radius: 13px !important;

        min-height: 48px !important;
    }


    .stTextInput > div > div > input:focus {

        border-color:
            #22c55e !important;

        box-shadow:
            0 0 0 1px
            rgba(34, 197, 94, 0.4) !important;
    }


    /* ========================================================
       CONTAINERS
    ======================================================== */

    [data-testid="stVerticalBlockBorderWrapper"] {

        background:
            rgba(10, 18, 13, 0.92);

        border:
            1px solid
            rgba(34, 197, 94, 0.10) !important;

        border-radius: 18px;
    }


    /* ========================================================
       EXPANDER
    ======================================================== */

    [data-testid="stExpander"] {

        background:
            rgba(10, 18, 13, 0.9);

        border:
            1px solid
            rgba(34, 197, 94, 0.10);

        border-radius: 15px;
    }


    /* ========================================================
       SIDEBAR
    ======================================================== */

    section[data-testid="stSidebar"] {

        background:
            #070b08;

        border-right:
            1px solid
            rgba(34, 197, 94, 0.10);
    }


    /* ========================================================
       TABLE
    ======================================================== */

    [data-testid="stDataFrame"] {

        border-radius: 12px;
    }


    /* ========================================================
       MOBILE
    ======================================================== */

    @media (max-width: 768px) {

        .main .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }

    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# LOAD CSV DATA
# ============================================================

@st.cache_data
def load_csv_data():

    customers = pd.DataFrame()
    products = pd.DataFrame()
    sales = pd.DataFrame()

    customers_file = DATA_DIR / "customers.csv"
    products_file = DATA_DIR / "products.csv"
    sales_file = DATA_DIR / "sales.csv"

    if customers_file.exists():
        customers = pd.read_csv(customers_file)

    if products_file.exists():
        products = pd.read_csv(products_file)

    if sales_file.exists():
        sales = pd.read_csv(sales_file)

    return customers, products, sales


# ============================================================
# LOAD DOCUMENTS
# ============================================================

@st.cache_data
def load_documents():

    documents = {}

    if DOCUMENTS_DIR.exists():

        for file in DOCUMENTS_DIR.glob("*.txt"):

            try:

                documents[file.name] = file.read_text(
                    encoding="utf-8"
                )

            except Exception:

                documents[file.name] = ""

    return documents


customers_df, products_df, sales_df = load_csv_data()

documents = load_documents()


# ============================================================
# BUSINESS CONTEXT
# ============================================================

def get_business_context():

    context = []

    if not customers_df.empty:

        context.append(
            "CUSTOMERS DATA:\n"
            + customers_df.to_string(index=False)
        )

    if not products_df.empty:

        context.append(
            "PRODUCTS DATA:\n"
            + products_df.to_string(index=False)
        )

    if not sales_df.empty:

        context.append(
            "SALES DATA:\n"
            + sales_df.to_string(index=False)
        )

    for filename, content in documents.items():

        context.append(
            f"{filename.upper()}:\n{content}"
        )

    return "\n\n====================\n\n".join(context)


# ============================================================
# GEMINI AI
# ============================================================

def ask_business_ai(question):

    if not GEMINI_API_KEY:

        return (
            "⚠️ **Gemini API key is not configured.**\n\n"
            "Please add `GEMINI_API_KEY` to your `.env` "
            "file or Streamlit Cloud Secrets."
        )

    business_context = get_business_context()

    prompt = f"""
You are BizAI, an AI Business Support System.

Your job is to answer questions using ONLY the
business information provided below.

BUSINESS INFORMATION:

{business_context}


USER QUESTION:

{question}


RULES:

1. Never invent business information.
2. Never invent prices.
3. Never invent customers.
4. Never invent sales.
5. Never invent policies.
6. Use the provided data for calculations.
7. If information is unavailable, clearly say:

"I don't have that information in the available business data."

8. Keep the answer professional.
9. Keep the answer easy to understand.
10. Use bullet points where useful.
11. If asking about a product, mention product name,
    product ID and price when available.

Answer the user's question.
"""

    try:

        client = genai.Client(
            api_key=GEMINI_API_KEY
        )

        for attempt in range(3):

            try:

                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=prompt,
                )

                if response and response.text:

                    return response.text

                return "No response received from Gemini."

            except Exception as e:

                error = str(e).lower()

                if (
                    "503" in error
                    or "unavailable" in error
                    or "overloaded" in error
                ):

                    if attempt < 2:

                        time.sleep(2)

                    else:

                        return (
                            "⚠️ Gemini is temporarily busy. "
                            "Please try again."
                        )

                else:

                    return f"⚠️ Gemini Error: {str(e)}"

    except Exception as e:

        return f"⚠️ Connection Error: {str(e)}"


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 🤖 BizAI")

    st.caption("Business Support System")

    st.divider()

    st.markdown("### Navigation")

    st.write("🏠 Home")
    st.write("✨ Features")
    st.write("🤖 AI Assistant")
    st.write("📊 Business Insights")
    st.write("📂 Business Data")
    st.write("ℹ️ About")

    st.divider()

    st.markdown("### AI Status")

    if GEMINI_API_KEY:

        st.success("● Gemini AI Connected")

    else:

        st.error("● Gemini API Key Missing")


# ============================================================
# NAVBAR
# ============================================================

with st.container(border=True):

    nav1, nav2 = st.columns([3, 1])

    with nav1:

        st.markdown("## 🤖 BizAI")

        st.caption("Business Support System")

    with nav2:

        if GEMINI_API_KEY:

            st.success("🟢 AI Online")

        else:

            st.error("🔴 AI Offline")


# ============================================================
# HERO
# ============================================================

st.write("")

st.markdown("### ✦ AI-POWERED BUSINESS SUPPORT")

st.title("Your Business.")

st.markdown("## 🟢 Smarter with AI.")

st.write(
    "Turn your business data into intelligent answers, "
    "useful insights, and smarter decisions with AI."
)

st.caption("🟢 Gemini AI Connected")


# ============================================================
# HERO BUTTONS
# ============================================================

hero1, hero2, hero3 = st.columns([1, 1, 1])

with hero2:

    b1, b2 = st.columns(2)

    with b1:

        try_ai = st.button(
            "🤖 Try AI Assistant",
            use_container_width=True
        )

    with b2:

        explore = st.button(
            "✨ Explore Features",
            use_container_width=True
        )


# ============================================================
# BUSINESS STATISTICS
# ============================================================

st.divider()

st.markdown("## 📊 Business at a Glance")

st.caption(
    "Real-time statistics from your business data."
)


total_customers = len(customers_df)

total_products = len(products_df)

total_sales = len(sales_df)


if not sales_df.empty:

    numeric_columns = sales_df.select_dtypes(
        include="number"
    ).columns

    if len(numeric_columns) > 0:

        total_sales_value = sales_df[
            numeric_columns[-1]
        ].sum()

    else:

        total_sales_value = 0

else:

    total_sales_value = 0


s1, s2, s3, s4 = st.columns(4)


with s1:

    st.metric(
        "👥 Customers",
        f"{total_customers:,}"
    )


with s2:

    st.metric(
        "📦 Products",
        f"{total_products:,}"
    )


with s3:

    st.metric(
        "🧾 Sales Records",
        f"{total_sales:,}"
    )


with s4:

    st.metric(
        "💰 Sales Value",
        f"₹{total_sales_value:,.0f}"
    )


# ============================================================
# FEATURES
# ============================================================

st.divider()

st.markdown("## ✨ Everything Your Business Needs")

st.caption(
    "One intelligent platform to understand your "
    "business data and make better decisions."
)


feature_data = [

    (
        "🤖",
        "AI Business Assistant",
        "Ask natural-language questions about your business "
        "and get intelligent answers using your real data."
    ),

    (
        "📊",
        "Sales Intelligence",
        "Analyze sales records and discover useful "
        "business insights."
    ),

    (
        "📦",
        "Product Intelligence",
        "Search products, prices and product information "
        "using AI."
    ),

    (
        "👥",
        "Customer Insights",
        "Understand customer information and business "
        "activity from your available data."
    ),

    (
        "📚",
        "Business Policy Assistant",
        "Ask questions about company policies, FAQs "
        "and return policies."
    ),

    (
        "🔍",
        "Business Data Search",
        "Search across your business data and documents "
        "using AI."
    ),
]


for row_start in range(0, len(feature_data), 3):

    row = feature_data[
        row_start:row_start + 3
    ]

    cols = st.columns(3)

    for col, feature in zip(cols, row):

        icon, title, description = feature

        with col:

            with st.container(border=True):

                st.markdown(
                    f"### {icon} {title}"
                )

                st.write(description)


# ============================================================
# AI ASSISTANT
# ============================================================

st.divider()

st.markdown("## 🤖 Meet Your AI Business Copilot")

st.caption(
    "Ask questions. Get answers. Make smarter decisions."
)


with st.container(border=True):

    st.markdown(
        "### 🤖 Business Intelligence Copilot"
    )

    st.caption(
        "Powered by Gemini + your real business data."
    )

    question = st.text_input(
        "Ask your business question",
        placeholder=(
            "Example: What is the price of Smart Watch?"
        )
    )

    ask_button = st.button(
        "🚀 Ask BizAI",
        use_container_width=True
    )


# ============================================================
# QUICK QUESTIONS
# ============================================================

st.markdown("### ⚡ Quick Questions")


q1, q2, q3, q4 = st.columns(4)

quick_question = None


with q1:

    if st.button(
        "💰 Product Prices",
        use_container_width=True
    ):

        quick_question = (
            "Show me all products and their prices."
        )


with q2:

    if st.button(
        "📊 Analyze Sales",
        use_container_width=True
    ):

        quick_question = (
            "Analyze the available sales data "
            "and give me useful business insights."
        )


with q3:

    if st.button(
        "📦 Product Details",
        use_container_width=True
    ):

        quick_question = (
            "Show me the available product details."
        )


with q4:

    if st.button(
        "📜 Return Policy",
        use_container_width=True
    ):

        quick_question = (
            "Explain the return policy."
        )


# ============================================================
# PROCESS AI QUESTION
# ============================================================

selected_question = None


if ask_button:

    selected_question = question


if quick_question:

    selected_question = quick_question


if try_ai:

    selected_question = ""


if selected_question is not None:

    if not selected_question.strip():

        st.info(
            "👋 Enter a business question above "
            "and click Ask BizAI."
        )

    else:

        st.divider()

        st.markdown("### 🧠 BizAI Response")

        with st.spinner(
            "BizAI is analyzing your business data..."
        ):

            answer = ask_business_ai(
                selected_question.strip()
            )

        with st.container(border=True):

            st.markdown(answer)


# ============================================================
# BUSINESS DATA
# ============================================================

st.divider()

st.markdown("## 📂 Your Business Data")

st.caption(
    "Explore the actual data used by BizAI."
)


with st.expander("🔍 View Business Data"):

    tab1, tab2, tab3 = st.tabs(
        [
            "👥 Customers",
            "📦 Products",
            "🧾 Sales"
        ]
    )

    with tab1:

        if not customers_df.empty:

            st.dataframe(
                customers_df,
                use_container_width=True
            )

        else:

            st.info(
                "No customer data available."
            )


    with tab2:

        if not products_df.empty:

            st.dataframe(
                products_df,
                use_container_width=True
            )

        else:

            st.info(
                "No product data available."
            )


    with tab3:

        if not sales_df.empty:

            st.dataframe(
                sales_df,
                use_container_width=True
            )

        else:

            st.info(
                "No sales data available."
            )


# ============================================================
# HOW IT WORKS
# ============================================================

st.divider()

st.markdown("## ⚙️ How BizAI Works")

st.caption(
    "Three simple steps to turn business data into intelligence."
)


h1, h2, h3 = st.columns(3)


with h1:

    with st.container(border=True):

        st.markdown("### 01")

        st.markdown(
            "#### 📂 Connect Your Data"
        )

        st.write(
            "BizAI reads your existing business "
            "data and documents."
        )


with h2:

    with st.container(border=True):

        st.markdown("### 02")

        st.markdown(
            "#### 🤖 Ask Your AI"
        )

        st.write(
            "Ask business questions using "
            "simple natural language."
        )


with h3:

    with st.container(border=True):

        st.markdown("### 03")

        st.markdown(
            "#### 💡 Get Intelligent Insights"
        )

        st.write(
            "Receive useful answers based on "
            "your actual business information."
        )


# ============================================================
# TECHNOLOGIES
# ============================================================

st.divider()

st.markdown("## 🛠️ Built With AI Technology")


tech1, tech2, tech3, tech4, tech5 = st.columns(5)


with tech1:

    st.info("🐍 Python")


with tech2:

    st.info("🎈 Streamlit")


with tech3:

    st.info("✨ Gemini AI")


with tech4:

    st.info("🧠 LangGraph")


with tech5:

    st.info("🔎 RAG")


# ============================================================
# ABOUT
# ============================================================

st.divider()

st.markdown("## ℹ️ About BizAI")

st.write(
    "BizAI is an AI-powered Business Support System "
    "that helps businesses understand their data, "
    "products, customers, sales and policies using "
    "natural-language AI."
)

st.write(
    "The system combines business data with Gemini AI "
    "to provide useful answers while reducing the risk "
    "of making up business information."
)


# ============================================================
# FINAL CTA
# ============================================================

st.divider()

st.markdown(
    "## 🚀 Ready to Make Your Business Smarter?"
)

st.caption(
    "Ask your business questions and let AI turn "
    "your data into useful insights."
)


cta1, cta2, cta3 = st.columns([1, 1, 1])


with cta2:

    if st.button(
        "🚀 Try BizAI Now",
        use_container_width=True
    ):

        st.info(
            "Scroll up to the AI Business Copilot "
            "and ask your question."
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown("## 🤖 BizAI")

st.caption(
    "Business Support System"
)

st.caption(
    "Python • Streamlit • Gemini AI"
)

st.caption(
    "© 2026 BizAI. All rights reserved."
)