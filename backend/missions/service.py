from uuid import uuid4
from backend.db import get_connection
from backend.models import Mission, MissionCreate, MissionStatus, utc_now


def create_mission(payload: MissionCreate) -> Mission:
    now = utc_now()
    mission = Mission(
        id=str(uuid4()), title=payload.title.strip(), description=payload.description.strip(),
        status=MissionStatus.PLANNED, priority=payload.priority,
        created_at=now, updated_at=now,
    )
    with get_connection() as connection:
        connection.execute(
            "INSERT INTO missions (id,title,description,status,priority,created_at,updated_at) VALUES (?,?,?,?,?,?,?)",
            (mission.id, mission.title, mission.description, mission.status.value, mission.priority,
             mission.created_at.isoformat(), mission.updated_at.isoformat()),
        )
    return mission


def list_missions(limit: int = 50) -> list[Mission]:
    with get_connection() as connection:
        rows = connection.execute(
            "SELECT * FROM missions ORDER BY created_at DESC LIMIT ?", (limit,)
        ).fetchall()
    return [Mission(**dict(row)) for row in rows]


def get_mission(mission_id: str) -> Mission | None:
    with get_connection() as connection:
        row = connection.execute("SELECT * FROM missions WHERE id = ?", (mission_id,)).fetchone()
    return Mission(**dict(row)) if row else None



def update_mission_status(mission_id: str, status: MissionStatus) -> Mission | None:
    now = utc_now()
    with get_connection() as connection:
        cursor = connection.execute(
            "UPDATE missions SET status = ?, updated_at = ? WHERE id = ?",
            (status.value, now.isoformat(), mission_id),
        )
        if cursor.rowcount == 0:
            return None
        row = connection.execute("SELECT * FROM missions WHERE id = ?", (mission_id,)).fetchone()
    return Mission(**dict(row)) if row else None
