from langchain.agents import initialize_agent, AgentType, Tool
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field
import os
from dotenv import load_dotenv

load_dotenv()

# 1. Initialize the LLM (The Brain)
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", temperature=0)

# 2. Define our Tools (The Hands)
def query_live_database(query: str) -> str:
    """Simulates querying the Postgres Database for live telemetry."""
    # In the next phase, we wire this to actual SQLAlchemy/Postgres
    print(f"🕵️ AGENT THOUGHT: Routing to Postgres SQL Database for: {query}")
    return "MOCK SQL RESULT: Freezer 404 temperature is currently -72°C. Status: Optimal."

def search_compliance_manuals(query: str) -> str:
    """Simulates searching the Qdrant Vector DB for PDF guidelines."""
    # In the next phase, we wire this to actual Qdrant embeddings
    print(f"🕵️ AGENT THOUGHT: Routing to Qdrant Vector DB for: {query}")
    return "MOCK VECTOR RESULT: According to GxP SOP Document v3, if a freezer drops below -70C, no action is required."

# 3. Package the Tools for LangChain
tools = [
    Tool(
        name="Live_Telemetry_DB",
        func=query_live_database,
        description="Use this tool ONLY when the user asks for current, live, or real-time status of systems, freezers, or servers."
    ),
    Tool(
        name="Compliance_Vector_DB",
        func=search_compliance_manuals,
        description="Use this tool ONLY when the user asks about standard operating procedures (SOP), compliance, manuals, or what to do in a situation."
    )
]

# 4. Initialize the Agent
omni_agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True, # This prints the Agent's internal thoughts to the terminal!
    handle_parsing_errors=True
)

def run_agent(user_query: str) -> str:
    """Executes the agent and returns the final answer."""
    try:
        response = omni_agent.invoke({"input": user_query})
        return response.get("output", "I could not find an answer.")
    except Exception as e:
        return f"Agent Error: {str(e)}"