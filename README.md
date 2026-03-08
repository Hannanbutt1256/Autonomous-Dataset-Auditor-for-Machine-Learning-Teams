# Autonomous Dataset Auditor MVP

A basic starter template combining FastAPI, CrewAI, Docker, and GitHub Actions for auditing datasets multi-agentically.

## Getting Started Locally

1. Copy `.env.example` to `.env` and add your LLM API keys. (e.g. `OPENAI_API_KEY`)
2. Build and run using Docker Compose:
   ```bash
   docker-compose up --build
   ```
3. Visit `http://localhost:8000/docs` to test the API via Swagger UI.

## File Structure

- `api/`: FastAPI routes and Pydantic schemas.
- `agents/`: CrewAI orchestrations, agents, and tasks.
- `.github/workflows/`: Basic CI pipeline for linting.
