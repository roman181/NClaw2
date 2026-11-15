# NClaw V1 Core – Quickstart

This first backend increment adds a local FastAPI service, a SQLite mission store, an agent registry and a deliberately non-executing Nexus stub. It does **not** yet connect Telegram or Ollama and does not execute shell commands or modify user files.

## Requirements

- Python 3.11+

## Start

```bash
python -m venv .venv
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Windows: copy .env.example .env
uvicorn backend.main:app --reload
```

The API binds to `127.0.0.1:8000` by default. Open `http://127.0.0.1:8000/docs` for interactive API documentation.

## First checks

```bash
curl http://127.0.0.1:8000/api/health
curl http://127.0.0.1:8000/api/agents
curl -X POST http://127.0.0.1:8000/api/missions -H "Content-Type: application/json" -d '{"title":"NClaw prüfen","description":"Ersten Missionstest durchführen","priority":"normal"}'
curl http://127.0.0.1:8000/api/missions
```

## Current scope and safety

- Missions are stored in `data/nclaw.db` (SQLite).
- The only registered agent is Nexus; it returns a planning outline and performs no actions.
- There is no shell/file execution, Telegram bot, Ollama integration, authentication, approval workflow or production deployment hardening yet.
- Keep the service on localhost. Do not expose it to the internet before authentication and authorization are implemented.
