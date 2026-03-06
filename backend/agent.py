from langchain.agents import create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain.memory import ConversationBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Qdrant
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase
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

# Create SQLDatabase instance for toolkit
db = SQLDatabase(engine)

# Setup Qdrant collection and vectorstore
def setup_vector_db():
    global vectorstore
    collections = qdrant_client.get_collections().collections
    collection_names = [c.name for c in collections]
    
    if "compliance_manuals" not in collection_names:
        qdrant_client.create_collection(
            collection_name="compliance_manuals",
            vectors_config=VectorParams(size=768, distance=Distance.COSINE),
        )
        
        loader = TextLoader("./data/sop.txt")
        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        docs = text_splitter.split_documents(documents)
        
        vectorstore = Qdrant.from_documents(
            docs,
            embeddings,
            url=os.getenv("QDRANT_URL"),
            collection_name="compliance_manuals",
        )
    else:
        # Collection exists, just connect to it
        vectorstore = Qdrant(
            client=qdrant_client,
            collection_name="compliance_manuals",
            embeddings=embeddings,
        )

# Call setup
setup_vector_db()

# 1. Initialize the LLM (The Brain)
llm = ChatGoogleGenerativeAI(model="models/gemini-flash-latest", temperature=0)

# 2. Define our Tools (The Hands)
def search_compliance_manuals(query: str) -> str:
    """Searches the Qdrant Vector DB for PDF guidelines."""
    print(f"🕵️ AGENT THOUGHT: Routing to Qdrant Vector DB for: {query}")
    try:
        docs = vectorstore.similarity_search(query, k=3)
        return "\n".join([doc.page_content for doc in docs])
    except Exception as e:
        return f"Vector search error: {str(e)}"

# Create SQL toolkit
sql_toolkit = SQLDatabaseToolkit(db=db, llm=llm)
sql_tools = sql_toolkit.get_tools()

# 3. Package the Tools for LangChain
tools = sql_tools + [
    Tool(
        name="Compliance_Vector_DB",
        func=search_compliance_manuals,
        description="Use this tool ONLY when the user asks about standard operating procedures (SOP), compliance, manuals, or what to do in a situation."
    )
]

# 4. Initialize the Agent with memory
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

prompt = PromptTemplate.from_template(
    "You are Omni-Agent, an enterprise AI assistant that routes queries between live telemetry databases and compliance manuals.\n\n"
    "Available tools:\n{tools}\n\n"
    "Tool names: {tool_names}\n\n"
    "Use the sql_db_query tool for questions about current status, live data, or telemetry.\n"
    "Use the sql_db_schema tool to understand database structure.\n"
    "Use the sql_db_list_tables tool to see available tables.\n"
    "Use the Compliance_Vector_DB tool for questions about procedures, compliance, or manuals.\n\n"
    "Chat History:\n{chat_history}\n\n"
    "Question: {input}\n"
    "Thought: {agent_scratchpad}"
)

agent = create_react_agent(llm, tools, prompt)
omni_agent = AgentExecutor(agent=agent, tools=tools, memory=memory, verbose=True, handle_parsing_errors=True)

def run_agent(user_query: str) -> str:
    """Executes the agent and returns the final answer."""
    try:
        response = omni_agent.invoke({"input": user_query})
        return response.get("output", "I could not find an answer.")
    except Exception as e:
        return f"Agent Error: {str(e)}"