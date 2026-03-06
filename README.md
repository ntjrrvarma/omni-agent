# 🛡️ Omni-Agent: Enterprise Context Engine

[![Docker](https://img.shields.io/badge/Docker-Ready-blue)](https://docker.com)
[![Python](https://img.shields.io/badge/Python-3.11+-green)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

An intelligent AI agent that bridges the gap between live operational data and historical compliance documents, solving enterprise data silos with dynamic query routing.

## 🎯 Problem Solved

Enterprise employees waste **20% of their workday** searching across scattered databases and PDF manuals. Traditional RAG systems only handle unstructured data. Omni-Agent intelligently routes queries to the right data source: **live SQL databases** for real-time status or **vector databases** for compliance procedures.

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐
│   Streamlit UI  │────│   FastAPI       │
│   (Frontend)    │    │   (Backend)     │
└─────────────────┘    └─────────────────┘
                                │
                    ┌───────────┼───────────┐
                    │           │           │
            ┌───────▼─────┐ ┌───▼─────┐ ┌───▼─────┐
            │ LangChain   │ │ Qdrant  │ │ Postgres│
            │ Agent       │ │ (Vector │ │ (SQL)   │
            │             │ │ DB)     │ │         │
            └─────────────┘ └─────────┘ └─────────┘
```

### Components

- **Frontend**: Streamlit chat interface for natural language queries
- **Backend**: FastAPI REST API with LangChain agent orchestration
- **Agent Brain**: LangChain ZERO_SHOT_REACT_DESCRIPTION agent with custom tools
- **Vector DB**: Qdrant for semantic search of compliance documents
- **SQL DB**: PostgreSQL for live operational data
- **Infrastructure**: Docker Compose for complete containerization

## ✨ Features

- 🤖 **Intelligent Routing**: Agent automatically determines query type and routes to appropriate database
- 🔍 **Vector Search**: Semantic search through compliance manuals and SOPs
- 🗃️ **SQL Queries**: Safe execution of live data queries
- 🐳 **Containerized**: One-command deployment with Docker
- 📊 **Real-time Data**: Live telemetry integration
- 📋 **Compliance Ready**: GxP and enterprise compliance focused
- 🚀 **Production Ready**: Health checks, error handling, and logging

## 🛠️ Tech Stack

- **AI/ML**: LangChain, Google Gemini 1.5 Flash
- **Backend**: FastAPI, Uvicorn
- **Frontend**: Streamlit
- **Databases**: Qdrant (Vector), PostgreSQL (Relational)
- **Embeddings**: Google Generative AI Embeddings
- **Infrastructure**: Docker, Docker Compose
- **Language**: Python 3.11+

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Google Gemini API key (free from [Google AI Studio](https://makersuite.google.com/app/apikey))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/ntjrrvarma/omni-agent.git
   cd omni-agent
   ```

2. **Configure environment**
   ```bash
   cp .env.example .env  # If exists, or edit .env
   # Add your GOOGLE_API_KEY to .env
   ```

3. **Launch the system**
   ```bash
   docker-compose up --build
   ```

4. **Access the application**
   - **Web Interface**: http://localhost:8501
   - **API Documentation**: http://localhost:8000/docs
   - **API Health**: http://localhost:8000/

## 💬 Usage Examples

### Query Routing in Action

**Live Data Query:**
```
User: "What's the current temperature of Freezer Unit 404?"
Agent: Routes to PostgreSQL → "Freezer 404 is currently -72°C. Status: Optimal."
```

**Compliance Query:**
```
User: "What is the SOP for freezer failure?"
Agent: Routes to Qdrant → Returns relevant sections from compliance manuals
```

### API Usage

```python
import requests

response = requests.post("http://localhost:8000/ask",
                        json={"question": "What is the current server status?"})
print(response.json())
```

## 📁 Project Structure

```
omni-agent/
├── backend/                 # FastAPI backend
│   ├── agent.py            # LangChain agent & tools
│   ├── main.py             # API endpoints
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile          # Backend container
├── frontend/               # Streamlit frontend
│   ├── app.py              # Chat interface
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile          # Frontend container
├── data/                   # Sample data & DB init
│   ├── sop.txt            # Sample compliance document
│   └── init.sql           # PostgreSQL seed data
├── docker-compose.yml      # Multi-service orchestration
├── .env                    # Environment variables
└── README.md              # This file
```

## 🔧 Configuration

### Environment Variables

```bash
# Database URLs
DATABASE_URL=postgresql://admin:password123@localhost:5432/omnidb
QDRANT_URL=http://localhost:6333

# AI Model
GOOGLE_API_KEY=your_gemini_api_key_here
```

### Customizing Data

- **Documents**: Add PDF/TXT files to `data/` directory
- **Database Schema**: Modify `data/init.sql` for custom tables
- **Agent Tools**: Extend tools in `backend/agent.py`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [LangChain](https://langchain.com) for agent orchestration
- Powered by [Google Gemini](https://ai.google.dev) for reasoning
- Vector search via [Qdrant](https://qdrant.tech)
- Containerization with [Docker](https://docker.com)

## 📞 Contact

**Your Name** - [LinkedIn](https://linkedin.com/in/yourprofile) - your.email@example.com

Project Link: [https://github.com/ntjrrvarma/omni-agent](https://github.com/ntjrrvarma/omni-agent)

---

*Built to demonstrate enterprise-grade AI agent development with real database integration and intelligent query routing.*