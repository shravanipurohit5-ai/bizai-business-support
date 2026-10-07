import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai


# ==============================
# PROJECT ROOT
# ==============================

BASE_DIR = Path(__file__).resolve().parent.parent


# ==============================
# LOAD .ENV
# ==============================

load_dotenv(BASE_DIR / ".env")


# ==============================
# GEMINI API KEY
# ==============================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found in .env file."
    )


# ==============================
# GEMINI CLIENT
# ==============================

client = genai.Client(
    api_key=GEMINI_API_KEY
)


# ==============================
# LOAD BUSINESS DOCUMENTS
# ==============================

def load_business_data():

    documents_folder = BASE_DIR / "documents"

    if not documents_folder.exists():
        return "No business documents folder found."

    all_data = []

    for file in documents_folder.glob("*.txt"):

        try:

            content = file.read_text(
                encoding="utf-8"
            )

            # Ignore empty files
            if content.strip():

                all_data.append(
                    f"\n--- {file.name} ---\n"
                    f"{content}"
                )

        except Exception as e:

            print(
                f"Could not read {file}: {e}"
            )

    if not all_data:
        return "No business information available."

    return "\n".join(all_data)


# ==============================
# ASK GEMINI
# ==============================

def ask_gemini(question):

    business_data = load_business_data()

    prompt = f"""
You are BizAI, a professional Business Support AI Assistant.

Your job is to answer the user's business questions using
the provided company information.

IMPORTANT RULES:

1. Use ONLY the business information provided below.
2. Do NOT invent company policies.
3. Do NOT give generic retailer information.
4. If the answer is not available in the business data,
   say exactly:

   "I could not find this information in our business data."

5. Give clear and professional answers.
6. Use bullet points when useful.
7. Keep the answer easy to understand.

========================
BUSINESS INFORMATION
========================

{business_data}

========================
USER QUESTION
========================

{question}

========================
ANSWER
========================
"""

    try:

        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:

        return f"Gemini Error: {str(e)}"