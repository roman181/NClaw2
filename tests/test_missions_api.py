from fastapi.testclient import TestClient

from backend.config import settings
from backend.main import app


def test_mission_lifecycle(tmp_path, monkeypatch):
    monkeypatch.setattr(settings, "data_dir", tmp_path)

    with TestClient(app) as client:
        created = client.post(
            "/api/missions",
            json={
                "title": "Dashboard testen",
                "description": "Mission anlegen und Status ändern",
                "priority": "high",
            },
        )
        assert created.status_code == 201
        mission = created.json()
        assert mission["status"] == "PLANNED"
        assert mission["priority"] == "high"

        listed = client.get("/api/missions")
        assert listed.status_code == 200
        assert [item["id"] for item in listed.json()] == [mission["id"]]

        changed = client.patch(
            f"/api/missions/{mission['id']}",
            json={"status": "RUNNING"},
        )
        assert changed.status_code == 200
        assert changed.json()["status"] == "RUNNING"

        detail = client.get(f"/api/missions/{mission['id']}")
        assert detail.status_code == 200
        assert detail.json()["status"] == "RUNNING"


def test_mission_validation_and_missing_status_target(tmp_path, monkeypatch):
    monkeypatch.setattr(settings, "data_dir", tmp_path)

    with TestClient(app) as client:
        invalid = client.post(
            "/api/missions",
            json={"title": "", "description": "Ungültiger Titel"},
        )
        assert invalid.status_code == 422

        missing = client.patch(
            "/api/missions/does-not-exist",
            json={"status": "COMPLETED"},
        )
        assert missing.status_code == 404
