from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from backend.agents.registry import registry
from backend.config import settings
from backend.db import init_db
from backend.models import HealthResponse, Mission, MissionCreate, MissionStatusUpdate
from backend.missions.service import create_mission, get_mission, list_missions, update_mission_status


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings.data_dir.mkdir(parents=True, exist_ok=True)
    init_db()
    yield


app = FastAPI(
    title="NClaw API",
    version="0.1.0",
    description="Local-first AI Office core. V1 currently manages missions; tool execution is intentionally disabled.",
    lifespan=lifespan,
)
# Local development only. Keep the API bound to 127.0.0.1 by default.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500", "http://127.0.0.1:8000", "http://localhost:8000"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "PATCH"],
    allow_headers=["Content-Type"],
)


@app.get("/api/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok", service="nclaw-api", database="sqlite")


@app.get("/api/system")
def system_status() -> dict:
    return {"name": "NClaw", "version": app.version, "status": "online", "mode": "local-first", "capabilities": ["mission-management", "agent-registry"]}


@app.get("/api/agents")
def agents() -> list[dict[str, str]]:
    return registry.list()


@app.post("/api/missions", response_model=Mission, status_code=201)
def post_mission(payload: MissionCreate) -> Mission:
    return create_mission(payload)


@app.get("/api/missions", response_model=list[Mission])
def missions(limit: int = Query(default=50, ge=1, le=200)) -> list[Mission]:
    return list_missions(limit)


@app.get("/api/missions/{mission_id}", response_model=Mission)
def mission_detail(mission_id: str) -> Mission:
    mission = get_mission(mission_id)
    if mission is None:
        raise HTTPException(status_code=404, detail="Mission not found")
    return mission


@app.patch("/api/missions/{mission_id}", response_model=Mission)
def patch_mission(mission_id: str, payload: MissionStatusUpdate) -> Mission:
    mission = update_mission_status(mission_id, payload.status)
    if mission is None:
        raise HTTPException(status_code=404, detail="Mission not found")
    return mission
