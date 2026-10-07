from langchain_ollama import ChatOllama

from mcp_server.tools import (
    search_customer,
    search_product,
    get_order,
    check_stock,
    get_sales_report,
    cancel_order,
    create_return,
)


llm = ChatOllama(
    model="llama3.2",
    temperature=0
)


def business_agent(state):

    question = state["question"]

    prompt = f"""
You are BizAI, an AI business support assistant.

Understand the user's request and provide the best answer.

Available business operations:

1. Customer search
2. Product search
3. Order details
4. Product stock
5. Sales report
6. Cancel order
7. Create return

User question:
{question}

Important:
- If the user asks about business data, use the appropriate business operation.
- Give a simple and professional answer.
"""

    response = llm.invoke(prompt)

    return {
        "question": question,
        "answer": response.content
    }