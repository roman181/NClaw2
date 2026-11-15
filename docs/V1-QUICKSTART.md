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

In a **second terminal**, serve the dashboard from the repository root:

```bash
python -m http.server 5500 --bind 127.0.0.1
```

Then open `http://127.0.0.1:5500/dashboard.html`. The dashboard can create missions, list stored missions and update their status. The API must remain running in the first terminal.

## First checks

```bash
curl http://127.0.0.1:8000/api/health
curl http://127.0.0.1:8000/api/agents
curl -X POST http://127.0.0.1:8000/api/missions -H "Content-Type: application/json" -d '{"title":"NClaw prüfen","description":"Ersten Missionstest durchführen","priority":"normal"}'
curl http://127.0.0.1:8000/api/missions
# Status einer Mission ändern (ID aus der POST-Antwort einsetzen):
curl -X PATCH http://127.0.0.1:8000/api/missions/ID -H "Content-Type: application/json" -d '{"status":"RUNNING"}'
```

## Current scope and safety

- Missions are stored in `data/nclaw.db` (SQLite).
- The only registered agent is Nexus; it returns a planning outline and performs no actions.
- There is no shell/file execution, Telegram bot, Ollama integration, authentication, approval workflow or production deployment hardening yet.
- Das Dashboard unterstützt das Anlegen von Missionen und das Ändern ihres Status.\n- `pytest -q` führt die API-Tests aus; GitHub Actions startet dieselben Tests bei Pushes und Pull Requests.\n- Keep the service on localhost. Do not expose it to the internet before authentication and authorization are implemented.
