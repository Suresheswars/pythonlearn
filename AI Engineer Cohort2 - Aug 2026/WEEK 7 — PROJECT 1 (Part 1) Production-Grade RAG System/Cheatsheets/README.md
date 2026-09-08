# Week 7 Cheatsheets

Printable quick-reference PDFs covering Week 7's Production-Grade RAG System
project: the layered application architecture, the FastAPI + Streamlit
two-process runtime, Dockerizing a multi-process app, a consolidated
reference for the `rag/` building blocks, and the local-dev-to-Render
deployment path. Each sheet also ends with an **Interview Prep** section of
likely interview Q&A for that topic.

| # | Cheatsheet | Covers |
|---|---|---|
| 1 | [Production RAG Architecture Cheatsheet](01_Production_RAG_Architecture_Cheatsheet.pdf) | Why layered design makes bugs findable, the frontend → API → services → rag/ call chain, the full request flow, diagnosing a bug by which layer owns the symptom. |
| 2 | [FastAPI + Streamlit Runtime Cheatsheet](02_FastAPI_Streamlit_Runtime_Cheatsheet.pdf) | Two processes in one container, internal-only FastAPI vs. public Streamlit, health-gated startup order, why `/docs` 404s on the live URL. |
| 3 | [Dockerizing a Multi-Process RAG App Cheatsheet](03_Dockerizing_Multi_Process_RAG_App_Cheatsheet.pdf) | One image across every environment, build/run commands, Dockerfile vs. entrypoint.sh responsibilities, verifying a build before shipping it. |
| 4 | [RAG Building Blocks Reference Cheatsheet](04_RAG_Building_Blocks_Reference_Cheatsheet.pdf) | The 10 files in `rag/` in pipeline order, choosing a retrieval strategy by symptom, where evaluation plugs into the request flow. |
| 5 | [Local Dev to Render Deployment Cheatsheet](05_Local_Dev_to_Render_Deployment_Cheatsheet.pdf) | Three ways to run the app, required environment variables, deploying to Render, what's identical vs. different between local Docker and deployed. |

## When to reach for which one

- New to the codebase and not sure where a piece of logic should live? → **01**
- Backend/frontend not talking to each other, or a race on startup? → **02**
- Docker build failing, or unsure what goes in the Dockerfile vs. entrypoint.sh? → **03**
- Picking a retrieval strategy for a symptom you're seeing? → **04**
- Ready to ship and need the deployment steps + env var checklist? → **05**
