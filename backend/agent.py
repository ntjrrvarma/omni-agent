from langchain.agents import initialize_agent, AgentType, Tool
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Qdrant
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize embeddings and clients
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
qdrant_client = QdrantClient(url=os.getenv("QDRANT_URL"))
engine = create_engine(os.getenv("DATABASE_URL"))

# Setup Qdrant collection and vectorstore
def setup_vector_db():
    qdrant_client.recreate_collection(
        collection_name="compliance_manuals",
        vectors_config=VectorParams(size=768, distance=Distance.COSINE),
    )
    
    loader = TextLoader("data/sop.txt")
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = text_splitter.split_documents(documents)
    
    global vectorstore
    vectorstore = Qdrant.from_documents(
        docs,
        embeddings,
        url=os.getenv("QDRANT_URL"),
        collection_name="compliance_manuals",
    )

# Call setup
setup_vector_db()

# 1. Initialize the LLM (The Brain)
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", temperature=0)

# 2. Define our Tools (The Hands)
def query_live_database(query: str) -> str:
    """Queries the Postgres Database for live telemetry data."""
    print(f"🕵️ AGENT THOUGHT: Routing to Postgres SQL Database for: {query}")
    try:
        # For demo, map natural queries to SQL
        if "404" in query or "freezer" in query.lower():
            with engine.connect() as conn:
                result = conn.execute(text("SELECT temperature, status FROM freezers WHERE unit_id = '404'"))
                row = result.fetchone()
                if row:
                    return f"Freezer 404 temperature is currently {row[0]}°C. Status: {row[1]}."
        return "No data found for that query."
    except Exception as e:
        return f"Database error: {str(e)}"

def search_compliance_manuals(query: str) -> str:
    """Searches the Qdrant Vector DB for PDF guidelines."""
    print(f"🕵️ AGENT THOUGHT: Routing to Qdrant Vector DB for: {query}")
    try:
        docs = vectorstore.similarity_search(query, k=3)
        return "\n".join([doc.page_content for doc in docs])
    except Exception as e:
        return f"Vector search error: {str(e)}"

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