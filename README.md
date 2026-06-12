---

title: Resume Analyzer
emoji: 📄
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
pinned: false
-------------

# 🚀RAG Based Resume Analyzing System
An AI-powered system that analyzes resumes against job descriptions using **Retrieval-Augmented Generation (RAG)** to provide **match scores, skill gaps, and actionable improvement suggestions.**

## Features
- Upload resume (PDF)
- Input job description (text or PDF)
- Semantic similarity matching using embeddings
- RAG-based intelligent retrieval
- Match score (0–100)
- Missing skills detection
- Personalized improvement suggestions
- Recommended skills to learn
- FastAPI backend with interactive frontend

## RAG Pipeline
```
User Input (Resume + Job Description)
        ↓
Text Extraction & Chunking
        ↓
Embedding Generation (OpenAI)
        ↓
Vector Storage (FAISS / Chroma)
        ↓
Semantic Retrieval
        ↓
LLM (Groq - Llama3)
        ↓
Structured Analysis Output
```

## System Design
```
Frontend (HTML/CSS/JS)
        │
        ▼
FastAPI Backend (main.py)
        │
        ▼
RAG Pipeline (pipeline.py)
        │
        ├── Loader
        ├── Chunking
        ├── Embeddings (OpenAI)
        ├── Vector Store (FAISS)
        ├── Retriever
        └── LLM (Groq)
        │
        ▼
JSON Response → Frontend UI

Frontend (HTML/CSS/JS)
```

## 📂 Project Structure
```
backend/
│
├── main.py                # FastAPI API routes
├── src/
│   ├── loader.py          # Load PDF/TXT files
│   ├── chunking.py        # Split text into chunks
│   ├── embeddings.py      # OpenAI embeddings
│   ├── vector_store.py    # FAISS/Chroma setup
│   ├── retriever.py       # Retrieval logic
│   ├── llm.py             # Groq LLM integration
│   └── pipeline.py        # Main RAG pipeline
│
├── data/                  # Sample data (optional)
├── notebooks/             # Experimental notebooks (ignored in production)
└── requirements.txt

frontend/
│
├── index.html
├── style.css
├── app.js
└── config.js
```

## Tech Stack
- Backend
  - FastAPI
  - Python
  - Uvicorn
- AI/ML
  - HuggingFace Embeddings (`sentence-transformers/all-MiniLM-L6-v2`)
  - Groq
  - LangChain
- Vector DB
  - FAISS/ChromaDB
- Frontend
  - HTML
  - CSS
  - JavaScript

## 🚀 Getting Started
### 1️⃣ Clone Repo
```
git clone https://github.com/SarthakMukherjee/Resume_analyse.git
cd Resume_analyze
```
### 2️⃣ Setup Backend
```
cd backend
python -m venv .venv
.venv\scripts\activate   # Windows
pip install -r requirements.txt
```
### 3️⃣ Setup Environment Variables
```
GROQ_API_KEY = your_api_key
```
### 4️⃣ 🏃 Run backend
```
uvicorn main:app --reload
```
Backend runs at (local environment):
```
http://127.0.0.1:8000
```
### 5️⃣ 🏃 Run Frontend
```
frontend/index.html
```
OR use Live Server (Recommended)

## Deployment
<<<<<<< HEAD
### Backend(HuggingFace)
=======
### Backend(Hugging Face Spaces - Docker)
>>>>>>> fd605c86cc0aeaffb20310df4c4078fb80a1eec8
Start command:
```
cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
```
ENV variables
- `GROQ_API_KEY`

**Dockerfile**
The project includes a `Dockerfile` at the root level which handles:
- Installing Python dependencies
- Setting up the application environment
- Starting the FastAPI server

**Application Startup**
The FastAPI application is served using Uvicorn: `uvicorn main:app --host 0.0.0.0 --port 7860`

Hugging Face Spaces requires applications to listen on port `7860`.

**Environment Variables**
Configure the following secrets in the Hugging Face Space settings:
- `GROQ_API_KEY`

Navigate to:
Space Settings → Repository Secrets 
and add the required environment variables.

**Deployment Steps**
- Create a new Hugging Face Space.
- Select Docker as the Space SDK.
- Upload the project files or connect te repository.
- Ensure the following files are present:
  - `Dockerfile`
  - `requirements.txt`
  - `main.py`
  - `backend/`
- Add the required environment variables in Space Secrets.
- Trigger a rebuild or Factory Reboot.

The application will be available at:
`https://hugingface.com/spaces/<username>/<space-name>`
  
### Frontend
Update in `config.js`:
```
API_BASE_URL: https://hugingface.com/spaces/<username>/<space-name>
```

## API Endpoints
- Health Check
```
GET /
```
- Analyze Resume + JD (.txt)
```
POST /analyze-text
```

## Example Output
```
{
  "success": true,
  "match_score": 92,
  "missing_skills": [
    "Experience with frontend tools: Although James has basic knowledge of HTML/CSS, ....",
    "Familiarity with business KPIs and reporting systems: While James has experience working with stakeholders to understand business metrics, ...",
    "Understanding of data pipelines: James has a basic ..."
  ],
  "improvement_suggestions": [
    "Develop a portfolio: Create a portfolio showcasing James' data visualization ....",
    "Enhance storytelling skills: While James has experience presenting insights to non-technical stakeholders, he may benefit ...",
    "Stay up-to-date with industry trends: James should stay current ..."
  ],
  "recommended_skills": [
    "Data pipeline management tools: Familiarity with tools like Apache ...",
    "Cloud-based data platforms: Knowledge of cloud-based data platforms like Amazon Web Services (AWS), ...",
    "Advanced data visualization tools: Experience with tools like D3.js, Plotly, ...",
    "Business acumen: Developing a deeper understanding of business operations, ..."
  ],
  "raw_analysis": "Match Score: 92\n\nThe candidate, James Dawson, has a strong background in data visualization, with experience in tools ....",
  "error": null   
}
```
