# StartupPilot AI

StartupPilot AI is a production-oriented SaaS application that helps founders transform a raw startup idea into a complete MVP plan using AI.

## What It Generates

- Startup overview, problem statement, target audience, personas
- Market, competitor, SWOT, Business Model Canvas, Lean Canvas
- Revenue model, pricing, acquisition, marketing
- Roadmap, MVP features, nice-to-have features
- Database schema, REST API design, authentication flow
- Architecture, ER diagram, frontend pages, Mermaid wireframes and flows
- Tech stack, deployment, cost, scaling, security
- AI recommendations, timeline, sprint plan, investor pitch, pitch deck outline, risk analysis

## Architecture

- Frontend: Next.js, TypeScript, Tailwind CSS, shadcn-style components, Framer Motion-ready
- Backend: FastAPI, Python, SQLAlchemy
- Database: PostgreSQL
- Auth: JWT and Google OAuth-ready boundary
- Cache: Redis
- Storage: Supabase Storage
- AI: OpenAI API, LangChain-ready orchestration, LlamaIndex-ready ingestion, ChromaDB-ready vector store
- Deployment: Docker, GitHub Actions, Railway, Vercel

## Repository Layout

```text
frontend/
backend/
database/
docker/
docs/
ai/
api/
tests/
scripts/
.github/
```

## Local Development

1. Copy `.env.example` to `.env` and set secrets.
2. Start services:

```powershell
docker compose up --build
```

3. API runs at `http://localhost:8000/api/v1`.
4. Frontend runs at `http://localhost:3000`.

## Current Implementation

This initial production scaffold includes:

- Executable FastAPI app factory
- Auth endpoints with JWT issuing
- Project and generation endpoints
- Complete deterministic startup planning engine
- Document upload and local RAG service
- PostgreSQL schema
- Next.js dashboard and generator UI
- Docker Compose stack
- GitHub Actions CI
- Backend unit tests

## Model-Backed Generators

The frontend generator pages call a server-side Next.js route at `POST /api/generate`.
That route uses the OpenAI Responses API and the configured model to generate real,
idea-specific outputs for Business Plan, Lean Canvas, Roadmap, Architecture, Investor
Readiness, and the other generator pages.

Create `frontend/.env.local` before running the frontend:

```env
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-5.5
```

Then restart the frontend:

```powershell
cd frontend
npm.cmd run dev
```

If `OPENAI_API_KEY` is missing, the app intentionally shows a configuration error
instead of falling back to fake local content.

## Important Production Notes

- Replace the local in-memory API stores with repository-backed PostgreSQL implementations before public launch.
- Add Alembic migrations for managed schema evolution.
- Configure OpenAI, Supabase Storage, Redis job queues, Google OAuth, and billing providers with production secrets.
- Keep generated reports citation-aware when using uploaded documents.
