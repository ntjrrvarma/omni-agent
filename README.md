🏗️ The Project: "Omni-Agent" (Enterprise Context Engine)
To impress companies like AstraZeneca (Pharma/Compliance), Microsoft (Enterprise SaaS), and Staples (Supply Chain/Retail), you need a project that solves a universal corporate nightmare: Data Silos.

The Pitch: “Enterprise employees waste 20% of their day searching for answers across scattered databases and PDF manuals. I built an Agentic AI system that intelligently routes queries to either live SQL databases or historical Vector databases to give them an instant answer.”

The "God Tier" Architecture Blueprint:
Frontend (The Interface): Streamlit (Python). It’s perfect for AI dashboards, looks clean, and takes 10% of the time to build compared to React.

Backend (The Engine): FastAPI. Lightning fast, handles the API requests.

The Brain (LangChain): Runs inside FastAPI. It uses an Agent with two specific tools:

Tool 1: Vector Search. Connects to Qdrant to search PDF documents.

Tool 2: SQL Query. Connects to Postgres to check live tabular data.

Databases:

Qdrant (Vector DB): Stores embeddings of PDF manuals (e.g., AstraZeneca GxP compliance docs, or Staples supply chain guidelines).

Postgres (Relational DB): Stores live dummy data (e.g., Live server status, or current warehouse inventory levels).

Infrastructure: Docker Compose spins all 4 layers up instantly.

🎬 How it plays out in an Interview (The Flex)
Imagine you are in the Microsoft or Staples interview. You open your laptop and show them the Streamlit UI.

You type Query 1: "What is the standard operating procedure for a freezer failure?"

What LangChain does: The Agent realizes this is a policy question. It uses the Vector DB Tool, searches Qdrant for the PDF manual, and generates an answer.

You type Query 2: "What is the current temperature of Freezer Unit 404?"

What LangChain does: The Agent realizes this requires live data. It ignores the Vector DB, uses the SQL Tool, queries your Postgres database, and returns: "Freezer 404 is currently at -70°C."

The Kill Shot (Why they hire you):
"I didn't just build a chat wrapper. I used LangChain to build a dynamic reasoning engine. In a company like yours, you have live operational data (Postgres) and static compliance data (PDFs/Qdrant). This architecture proves I can securely bridge GenAI with both."

💼 The LinkedIn Post Strategy
When we finish this, your post will look like this:

"Retrieval-Augmented Generation (RAG) is great, but it's not enough for enterprise scale. A real business needs AI that can query live SQL databases AND search unstructured PDFs simultaneously.

This weekend, I built an 'Omni-Agent' using LangChain, FastAPI, Qdrant, and Postgres, fully containerized with Docker.

Instead of forcing every query through a vector search, my LangChain Agent dynamically routes the user's question: if it's a policy question, it searches the Vector DB. If it's a live status question, it safely generates and executes a SQL query against Postgres.

Here is a deep dive into how I built the LangChain routing logic to prevent SQL injection and hallucination... [Link to GitHub]"

## 🚀 How to Run

1. **Clone the repo:**
   ```bash
   git clone https://github.com/ntjrrvarma/omni-agent.git
   cd omni-agent
   ```

2. **Set up environment:**
   - Copy `.env` and add your Google Gemini API key
   - Ensure Docker is installed

3. **Launch the system:**
   ```bash
   docker-compose up --build
   ```

4. **Access the interfaces:**
   - Frontend (Streamlit): http://localhost:8501
   - Backend API: http://localhost:8000/docs (FastAPI docs)

5. **Test queries:**
   - "What is the current temperature of Freezer Unit 404?"
   - "What is the standard operating procedure for a freezer failure?"

The system will automatically route queries to the appropriate database!