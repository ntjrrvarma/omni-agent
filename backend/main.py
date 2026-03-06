from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from dotenv import load_dotenv

# LangChain & Qdrant imports
from langchain_google_genai import ChatGoogleGenerativeAI
from qdrant_client import QdrantClient

# Load Environment Variables
load_dotenv()

# Initialize FastAPI
app = FastAPI(title="Omni-Agent Enterprise API", version="1.0")

# Initialize LLM Brain (Gemini Pro)
llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.2)

# Initialize Qdrant Vector DB Connection
try:
    qdrant = QdrantClient(url=os.getenv("QDRANT_URL"))
    # Check if DB is alive
    qdrant.get_collections()
    db_status = "Connected 🟢"
except Exception as e:
    db_status = f"Disconnected 🔴 ({str(e)})"

# --- API Models ---
class QueryRequest(BaseModel):
    question: str

# --- API Routes ---
@app.get("/")
def health_check():
    """System Health Monitor"""
    return {
        "status": "Omni-Agent is Alive",
        "vector_db": db_status,
        "llm": "Ready"
    }

@app.post("/ask")
def ask_omni_agent(request: QueryRequest):
    """The main routing endpoint for the AI"""
    try:
        # For Phase 1, we just do a direct LLM call to prove it works.
        # In Phase 2, we will add the SQL/Vector routing Agent here.
        response = llm.invoke(request.question)
        return {"question": request.question, "answer": response.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))