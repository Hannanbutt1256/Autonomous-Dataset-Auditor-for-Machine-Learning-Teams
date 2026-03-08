# 🔍 Autonomous Dataset Auditor for ML Teams

> A multi-agent AI system that autonomously audits datasets for machine learning readiness — detecting schema issues, bias, data leakage, quality problems, and more — then generates a production-ready preprocessing pipeline.

---

## 🚀 Overview

The **Autonomous Dataset Auditor** is a FastAPI-powered backend that orchestrates a **9-agent CrewAI pipeline** to perform a comprehensive audit of any CSV or Excel dataset. Simply provide a dataset URL, and the system returns a structured audit report covering every critical dimension of ML readiness.

---

## 🤖 Agent Pipeline

The system runs **9 specialized AI agents** sequentially, each responsible for a distinct audit dimension:

| # | Agent | Responsibility |
|---|-------|---------------|
| 1 | **Schema Auditor** | Infers dataset domain, column types, missing values, and column roles (feature / target / identifier) |
| 2 | **Bias & Fairness Auditor** | Detects class imbalance, sensitive attributes, and demographic representation risks |
| 3 | **Leakage Detection Specialist** | Identifies direct, proxy, temporal, and ID-based target leakage risks |
| 4 | **Data Quality Auditor** | Finds duplicates, outliers, skewed distributions, invalid values, and constant columns |
| 5 | **Feature Readiness Analyst** | Evaluates feature suitability — redundancy, high cardinality, correlation, encoding/scaling needs |
| 6 | **Preprocessing Strategist** | Designs a complete preprocessing plan based on all prior findings |
| 7 | **Model Compatibility Advisor** | Recommends suitable ML algorithms based on dataset characteristics |
| 8 | **Pipeline Code Generator** | Generates a complete, executable Python preprocessing pipeline using pandas & scikit-learn |
| 9 | **Audit Report Generator** | Consolidates all findings into a structured JSON report conforming to the Pydantic schema |

---

## 🛠️ Tech Stack

- **[FastAPI](https://fastapi.tiangolo.com/)** — REST API framework
- **[CrewAI](https://www.crewai.com/)** — Multi-agent orchestration (sequential pipeline)
- **[OpenAI GPT-4o-mini](https://platform.openai.com/)** — LLM backbone for all agents
- **[Pydantic](https://docs.pydantic.dev/)** — Request/response schema validation
- **[Docker](https://www.docker.com/)** — Containerized deployment
- **[GitHub Actions](https://github.com/features/actions)** — CI/CD pipeline

---

## 📁 Project Structure

```
Autonomous Dataset Auditor/
├── api/
│   ├── main.py          # FastAPI app, /health and /api/audit endpoints
│   └── models.py        # Pydantic schemas: AuditRequest, AuditResponse, DatasetSummary
├── agents/
│   ├── agents.py        # 9 CrewAI agent definitions
│   ├── tasks.py         # 9 task definitions with prompts and expected outputs
│   └── crew.py          # AuditorCrew: assembles and runs the sequential pipeline
├── .github/
│   └── workflows/       # GitHub Actions CI pipeline
├── Dockerfile           # Docker build config (Python 3.11, uvicorn on port 8000)
├── requirements.txt     # Python dependencies
└── .env                 # API keys (not committed)
```

---

## 📦 API Reference

### `GET /health`
Returns service health status.

**Response:**
```json
{"status": "ok"}
```

---

### `POST /api/audit`
Triggers the full 9-agent dataset audit pipeline.

**Request Body:**
```json
{
  "dataset_url": "https://example.com/dataset.csv",
  "target_column": "target"
}
```

**Response (`AuditResponse`):**
```json
{
  "status": "completed",
  "dataset_url": "...",
  "summary": {
    "dataset_name": "...",
    "rows": 1000,
    "columns": 15,
    "domain": "finance",
    "ml_readiness": "medium",
    "bias_risk": "high",
    "leakage_risk": "low",
    "data_quality_risk": "medium",
    "feature_readiness_risk": "low",
    "preprocessing_plan_risk": "low",
    "model_compatibility_risk": "low",
    "pipeline_code_risk": "low"
  },
  "schema_analysis": { ... },
  "bias_analysis": { ... },
  "leakage_analysis": { ... },
  "data_quality_analysis": { ... },
  "feature_readiness_analysis": { ... },
  "preprocessing_plan": { ... },
  "model_compatibility_analysis": { ... },
  "recommendations": ["...", "..."],
  "pipeline_code": "import pandas as pd\n...",
  "human_report": "# Dataset Audit Report\n..."
}
```

---

## ⚙️ Getting Started

### Prerequisites

- Python 3.11+
- Docker & Docker Compose
- An OpenAI API key

### 1. Configure Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

### 2. Run with Docker

```bash
docker build -t dataset-auditor .
docker run -p 8000:8000 --env-file .env dataset-auditor
```

### 3. Run Locally (without Docker)

```bash
# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate       # Windows
source venv/bin/activate    # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn api.main:app --reload
```

### 4. Access the API

- **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🧪 Example Usage

```bash
curl -X POST http://localhost:8000/api/audit \
  -H "Content-Type: application/json" \
  -d '{"dataset_url": "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv", "target_column": "Survived"}'
```

---

## 📋 Dependencies

```
fastapi
uvicorn
pydantic
crewai[tools]
crewai[anthropic]
```

---

## 🔄 CI/CD

A GitHub Actions workflow is included under `.github/workflows/` for automated linting on every push and pull request.

---

## 📄 License

This project is open-source. Feel free to use and extend it for your ML team's dataset auditing needs.
