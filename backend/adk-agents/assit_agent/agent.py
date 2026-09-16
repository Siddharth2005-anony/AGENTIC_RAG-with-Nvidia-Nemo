from google.adk.agents import Agent

from .tools import (
    query_sqlite,
    search_milvus
)


root_agent = Agent(
    name="hybrid_rag_agent",

    model="gemini-2.5-flash",

    description=(
        "An agent that retrieves structured data "
        "from SQLite and documents from Milvus."
    ),

    instruction="""
    You are a company knowledge assistant.

    You have exactly two tools:

    1. query_sqlite
       Use for financial questions:
       - Revenue
       - Expenses
       - Profit
       - Financial quarters

    2. search_milvus
       Use for:
       - Company documents
       - Policies
       - Reports
       - General knowledge

    TOOL SELECTION:

    - Financial figures and structured data:
      use query_sqlite.

    - Document-based or general knowledge questions:
      use search_milvus.

    - If a question requires information from both sources,
      use both tools.

    - Never invent financial figures.

    - Answer clearly using the retrieved information.
    """,

    tools=[
        query_sqlite,
        search_milvus
    ]
)