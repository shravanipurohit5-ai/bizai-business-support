import os
import time
from pathlib import Path

import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from google import genai


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="BizAI - Business Support",
    page_icon="🤖",
    layout="wide"
)


# ==========================================
# PROJECT PATH
# ==========================================

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DOCUMENTS_DIR = BASE_DIR / "documents"


# ==========================================
# LOAD ENVIRONMENT
# ==========================================

load_dotenv(BASE_DIR / ".env")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


# ==========================================
# LOAD CSV DATA
# ==========================================

def load_csv_data():

    business_data = []

    # --------------------------------------
    # CUSTOMERS
    # --------------------------------------

    customers_file = DATA_DIR / "customers.csv"

    if customers_file.exists():

        try:

            customers = pd.read_csv(
                customers_file
            )

            if not customers.empty:

                business_data.append(
                    "CUSTOMERS DATA:\n"
                    + customers.to_string(
                        index=False
                    )
                )

        except Exception as e:

            business_data.append(
                f"Customers data error: {e}"
            )


    # --------------------------------------
    # PRODUCTS
    # --------------------------------------

    products_file = DATA_DIR / "products.csv"

    if products_file.exists():

        try:

            products = pd.read_csv(
                products_file
            )

            if not products.empty:

                business_data.append(
                    "PRODUCTS DATA:\n"
                    + products.to_string(
                        index=False
                    )
                )

        except Exception as e:

            business_data.append(
                f"Products data error: {e}"
            )


    # --------------------------------------
    # SALES
    # --------------------------------------

    sales_file = DATA_DIR / "sales.csv"

    if sales_file.exists():

        try:

            sales = pd.read_csv(
                sales_file
            )

            if not sales.empty:

                business_data.append(
                    "SALES DATA:\n"
                    + sales.to_string(
                        index=False
                    )
                )

        except Exception as e:

            business_data.append(
                f"Sales data error: {e}"
            )


    if not business_data:

        return "No CSV business data is available."

    return "\n\n".join(
        business_data
    )


# ==========================================
# LOAD BUSINESS DOCUMENTS
# ==========================================

def load_documents():

    document_data = []

    if not DOCUMENTS_DIR.exists():

        return "No business documents available."


    for file in DOCUMENTS_DIR.glob("*.txt"):

        try:

            content = file.read_text(
                encoding="utf-8"
            )

            if content.strip():

                document_data.append(
                    f"--- {file.name} ---\n"
                    f"{content}"
                )

        except Exception as e:

            document_data.append(
                f"{file.name}: Error reading file"
            )


    if not document_data:

        return "No business documents available."


    return "\n\n".join(
        document_data
    )


# ==========================================
# COMBINE ALL BUSINESS DATA
# ==========================================

def get_all_business_data():

    csv_data = load_csv_data()

    documents = load_documents()

    return f"""
==============================
BUSINESS DOCUMENTS
==============================

{documents}


==============================
BUSINESS CSV DATA
==============================

{csv_data}
"""


# ==========================================
# ASK GEMINI
# ==========================================

def ask_business_ai(question):

    if not GEMINI_API_KEY:

        return (
            "GEMINI_API_KEY was not found "
            "in your .env file."
        )


    business_data = get_all_business_data()


    # ======================================
    # PROMPT
    # ======================================

    prompt = f"""
You are BizAI, a professional Business
Support AI Assistant.

Answer the user's question using ONLY
the business information provided below.

IMPORTANT RULES:

1. Use only the provided business data.
2. Do NOT invent business information.
3. Do NOT provide generic retailer information.
4. If information is unavailable, say:

"I could not find this information in
our business data."

5. For product questions, use PRODUCTS DATA.
6. For customer questions, use CUSTOMERS DATA.
7. For sales questions, use SALES DATA.
8. For return-policy questions, use
   BUSINESS DOCUMENTS.
9. Perform simple calculations when required.
10. Give clear and professional answers.
11. Use bullet points when useful.

==============================
BUSINESS INFORMATION
==============================

{business_data}

==============================
USER QUESTION
==============================

{question}

==============================
ANSWER
==============================
"""


    # ======================================
    # GEMINI CLIENT
    # ======================================

    try:

        client = genai.Client(
            api_key=GEMINI_API_KEY
        )


        # ==================================
        # RETRY FOR TEMPORARY 503 ERROR
        # ==================================

        for attempt in range(3):

            try:

                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=prompt
                )

                return response.text


            except Exception as e:

                error_message = str(e)


                # --------------------------
                # GEMINI TEMPORARY ERROR
                # --------------------------

                if (
                    "503" in error_message
                    or "UNAVAILABLE"
                    in error_message
                ):

                    if attempt < 2:

                        wait_time = 2 ** attempt

                        time.sleep(
                            wait_time
                        )

                        continue


                    return (
                        "⚠️ Gemini is temporarily "
                        "busy because of high demand.\n\n"
                        "Please click **Ask AI** again "
                        "after a few seconds."
                    )


                # --------------------------
                # OTHER GEMINI ERROR
                # --------------------------

                return (
                    f"Gemini Error: "
                    f"{error_message}"
                )


    except Exception as e:

        return (
            f"Gemini Connection Error: "
            f"{str(e)}"
        )


# ==========================================
# STREAMLIT UI
# ==========================================

st.title(
    "🤖 BizAI - AI Business Support System"
)

st.write(
    "Your AI-powered business assistant"
)


# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.header("📊 Business Data")

    st.write(
        "Connected data sources:"
    )

    st.success(
        "✅ Customers CSV"
    )

    st.success(
        "✅ Products CSV"
    )

    st.success(
        "✅ Sales CSV"
    )

    st.success(
        "✅ Business Documents"
    )

    st.divider()

    if GEMINI_API_KEY:

        st.success(
            "🔑 Gemini API Connected"
        )

    else:

        st.error(
            "❌ Gemini API Key Missing"
        )

    st.caption(
        "Powered by Gemini AI"
    )


# ==========================================
# QUESTION INPUT
# ==========================================

question = st.text_input(
    "Ask your business question:",
    placeholder=(
        "Example: What is the price "
        "of Smart Watch?"
    )
)


# ==========================================
# ASK AI BUTTON
# ==========================================

if st.button(
    "🤖 Ask AI",
    use_container_width=True
):

    if question.strip():

        with st.spinner(
            "BizAI is analyzing your "
            "business data..."
        ):

            response = ask_business_ai(
                question
            )


        st.subheader(
            "💡 AI Response"
        )

        st.write(
            response
        )

    else:

        st.warning(
            "Please enter a question."
        )