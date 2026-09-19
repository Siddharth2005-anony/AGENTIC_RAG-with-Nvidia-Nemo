# Agentic RAG Pipeline

An enterprise-grade Retrieval-Augmented Generation (RAG) system with a React frontend and FastAPI backend. Features document ingestion, semantic search, vector storage with Milvus, NVIDIA embeddings, and OpenAI-powered grounded responses.

## Architecture Overview

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Frontend      │     │    Backend      │     │   Database      │
│   (React/Vite)  │────▶│   (FastAPI)     │────▶│   (Milvus)      │
│   Port: 5173    │     │   Port: 8000    │     │   (demo.db)     │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   LLM &         │
                       │   Embeddings    │
                       │   (OpenAI +     │
                       │   NVIDIA)       │
                       └─────────────────┘
```

## Features

### Backend (FastAPI)
- **Document Upload**: PDF, TXT, DOCX support with automatic text extraction, cleaning, and chunking
- **Vector Embeddings**: NVIDIA Nemotron-3-Embed-1B via LangChain
- **Vector Database**: Milvus Lite for local persistent storage with cosine similarity search
- **RAG Pipeline**: Query embedding → vector search → grounded LLM response (GPT-4.1-mini)
- **Collection Management**: List, create, and delete document collections
- **Google ADK Agent**: Hybrid RAG agent supporting both Milvus (documents) and SQLite (structured data)

### Frontend (React + Vite)
- **Chat Interface**: Real-time conversation with latency metrics
- **Document Upload**: Drag-and-drop file upload with progress feedback
- **Collection Explorer**: View and manage stored document collections
- **Responsive UI**: Clean, enterprise-style design with status indicators

## Tech Stack

| Layer | Technology |
|-------|------------|
| **Backend** | FastAPI, Uvicorn, Pydantic |
| **Vector DB** | Milvus (via pymilvus + milvus-lite) |
| **Embeddings** | NVIDIA Nemotron-3-Embed-1B (langchain-nvidia-ai-endpoints) |
| **LLM** | OpenAI GPT-4.1-mini |
| **Document Processing** | PyMuPDF, python-docx, langchain-text-splitters |
| **Frontend** | React 19, Vite, Axios |
| **Containerization** | Docker, Docker Compose, Nginx |
| **Agent Framework** | Google ADK (Agent Development Kit) |

## Quick Start

### Prerequisites
- Docker & Docker Compose
- NVIDIA API Key (for embeddings)
- OpenAI API Key (for LLM responses)

### Environment Setup

Create `backend/.env`:
```env
NVIDIA_API_KEY=your_nvidia_api_key
OPENAI=your_openai_api_key
```

### Run with Docker Compose (Recommended)

```bash
# Build images (first time or after Dockerfile changes)
docker compose build

# Start all services (backend + frontend + nginx)
docker compose up -d

# View logs
docker compose logs -f

# Stop everything
docker compose down
```

**Access Points:**
- Frontend: http://localhost (via Nginx on port 80)
- Backend API: http://localhost/api (proxied through Nginx)
- Direct Backend: http://localhost:8000
- Direct Frontend Dev: http://localhost:5173

### Manual Development Setup

**Backend:**
```bash
cd backend
pip install -r reqs.txt
cp .env.example .env  # Add your API keys
uvicorn main_rag:app --reload --host 0.0.0.0 --port 8000
```

**Frontend:**
```bash
cd frontend-rag/react
npm install
npm run dev
```

## API Endpoints

### Chat & Query
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/NVIDIA` | Submit a query to the RAG pipeline |
| `GET` | `/documents/{n}` | Retrieve document by ID |

### Document Management
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/upload` | Upload and process a document (PDF, TXT, DOCX) |
| `GET` | `/collections` | List all Milvus collections |
| `DELETE` | `/collections/{name}` | Delete a collection by name |
| `DELETE` | `/del_col` | Legacy delete endpoint |

### Request/Response Examples

**Query:**
```bash
curl -X POST http://localhost:8000/NVIDIA \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the capital of Japan?"}'
```

**Response:**
```json
{
  "answer": "The capital of Japan is Tokyo."
}
```

**Upload:**
```bash
curl -X POST http://localhost:8000/upload \
  -F "file=@document.pdf"
```

**Response:**
```json
{
  "status": "success",
  "filename": "document.pdf",
  "chunks": 12
}
```

## Project Structure

```
AG_RAG_NW/
├── backend/
│   ├── main_rag.py              # FastAPI app entry point
│   ├── reqs.txt                 # Python dependencies
│   ├── Dockerfile.backend       # Backend container
│   ├── .env                     # Environment variables (create this)
│   ├── config/
│   │   └── settings.py          # Configuration management
│   ├── routes/
│   │   ├── chats.py             # Query & collection endpoints
│   │   └── upload.py            # Document upload pipeline
│   ├── intelligence/
│   │   ├── embedder.py          # NVIDIA embeddings wrapper
│   │   └── llm_feeder.py        # OpenAI LLM integration
│   ├── database/
│   │   ├── milvus_client.py     # Milvus operations
│   │   └── pineapple.py         # Alternative vector DB
│   ├── clerks/                  # Document processing pipeline
│   │   ├── validator.py         # File validation
│   │   ├── loader.py            # Text extraction (PDF/DOCX/TXT)
│   │   ├── cleaner.py           # Text cleaning
│   │   ├── splitter.py          # Document chunking
│   │   └── metadata.py          # Metadata generation
│   ├── adk-agents/
│   │   └── assist_agent/        # Google ADK hybrid RAG agent
│   │       ├── agent.py         # Agent definition
│   │       ├── tools.py         # Tool implementations
│   │       ├── vec_db.py        # Milvus tool
│   │       └── sqlite3.py       # SQLite tool
│   └── storage/
│       └── uploads/             # Stored uploaded files
├── frontend-rag/
│   └── react/
│       ├── package.json
│       ├── Dockerfile
│       ├── vite.config.js
│       ├── src/
│       │   ├── App.jsx          # Main application component
│       │   ├── About.jsx        # About page
│       │   ├── main.jsx         # Entry point
│       │   └── App.css          # Styles
│       └── public/
├── docker-compose.yml           # Multi-service orchestration
├── Dockerfile.nginx             # Nginx reverse proxy
└── README.md
```

## Document Processing Pipeline

```
Upload → Validate → Save → Extract Text → Clean → Chunk → Embed → Store in Milvus
         │                                                    │
         └────────────────────── Metadata ──────────────────┘
```

1. **Validation**: File type (PDF/TXT/DOCX) and size checks
2. **Extraction**: PyMuPDF for PDF, python-docx for DOCX, native for TXT
3. **Cleaning**: Whitespace normalization, artifact removal
4. **Chunking**: Semantic splitting with overlap (LangChain)
5. **Embedding**: NVIDIA Nemotron-3-Embed-1B (1024/2048 dim)
6. **Storage**: Milvus with cosine similarity index

## Configuration

Key settings in `backend/config/settings.py`:
- `TOP_K`: Number of retrieved chunks (default: 5)
- `NVIDIA_API_KEY`: Required for embeddings
- `OPENAI`: Required for LLM responses
- `OLLAMA_BASE_URL`: Optional local LLM fallback
- `REDIS_*`: Optional Redis configuration

## Google ADK Agent

The `adk-agents/assist_agent` implements a hybrid RAG agent with two tools:
- **query_sqlite**: Financial/structured data queries
- **search_milvus**: Document-based semantic search

Model: `gemini-2.5-flash`

## Docker Services

| Service | Port | Description |
|---------|------|-------------|
| `backend` | 8000 | FastAPI application |
| `frontend` | 5173 | Vite dev server |
| `nginx` | 80 | Reverse proxy (production) |

Nginx routes:
- `/` → Frontend
- `/api/` → Backend

## Troubleshooting

**Milvus dimension mismatch**: The chat endpoint uses 1024-dim, upload uses 2048-dim. Ensure consistency or use separate collections.

**API key errors**: Verify `.env` file exists in `backend/` with valid `NVIDIA_API_KEY` and `OPENAI`.

**Port conflicts**: Ensure ports 80, 5173, 8000 are available.

**Frontend can't reach backend**: Check Nginx config or use direct backend URL in development.

## License

MIT License - Feel free to use and modify for your projects.
