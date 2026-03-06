from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient

# IMPORT OUR NEW AGENT
from agent import run_agent

load_dotenv()

app = FastAPI(title="Omni-Agent Enterprise API", version="1.0")

try:
    qdrant = QdrantClient(url=os.getenv("QDRANT_URL"))
    qdrant.get_collections()
    db_status = "Connected 🟢"
except Exception as e:
    db_status = f"Disconnected 🔴 ({str(e)})"

class QueryRequest(BaseModel):
    question: str

@app.get("/")
def health_check():
    return {
        "status": "Omni-Agent is Alive",
        "vector_db": db_status,
        "agent": "Ready to Route"
    }

@app.post("/ask")
def ask_omni_agent(request: QueryRequest):
    """The main routing endpoint for the AI"""
    try:
        # NOW WE CALL THE AGENT INSTEAD OF THE RAW LLM
        answer = run_agent(request.question)
        return {"question": request.question, "answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))