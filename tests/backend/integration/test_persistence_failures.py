import sqlite3

from fastapi.testclient import TestClient
import pytest

from app import api as api_package
from app.api import meals as meals_api
from app.api import targets as targets_api
from app.main import app


def meal_payload(**overrides):
    payload = {
        "name": "Toast",
        "category": "Breakfast",
        "date": "2026-10-28",
        "quantity": "1.00",
        "calories_per_serving": "100.00",
        "protein_per_serving": "4.00",
    }
    payload.update(overrides)
    return payload


@pytest.fixture

def client(tmp_path, monkeypatch):
    monkeypatch.setenv("CALORIE_TRACKER_DATA_DIR", str(tmp_path))
    with TestClient(app, base_url="http://127.0.0.1") as test_client:
        yield test_client


def fail_write(*_args, **_kwargs):
    raise sqlite3.OperationalError("simulated local database failure")


def test_failed_create_does_not_report_success_or_add_entry(client, monkeypatch):
    monkeypatch.setattr(meals_api, "create_meal", fail_write)

    response = client.post("/api/meals", json=meal_payload())
    day = client.get("/api/days/2026-10-28").json()

    assert response.status_code == 500
    assert response.json()["error"]["code"] == "persistence_failed"
    assert day["meals"] == []
    assert day["summary"]["calories"]["intake"] == "0.00"


def test_failed_edit_preserves_last_saved_entry(client, monkeypatch):
    created = client.post("/api/meals", json=meal_payload()).json()
    monkeypatch.setattr(meals_api, "replace_meal", fail_write)

    response = client.put(f"/api/meals/{created['id']}", json=meal_payload(quantity="2.00"))
    day = client.get("/api/days/2026-10-28").json()

    assert response.status_code == 500
    assert response.json()["error"]["code"] == "persistence_failed"
    assert day["meals"][0]["quantity"] == "1.00"
    assert day["summary"]["calories"]["intake"] == "100.00"


def test_failed_delete_preserves_last_saved_entry(client, monkeypatch):
    created = client.post("/api/meals", json=meal_payload()).json()
    monkeypatch.setattr(meals_api, "delete_meal", fail_write)

    response = client.delete(f"/api/meals/{created['id']}")
    day = client.get("/api/days/2026-10-28").json()

    assert response.status_code == 500
    assert response.json()["error"]["code"] == "persistence_failed"
    assert len(day["meals"]) == 1
    assert day["summary"]["calories"]["intake"] == "100.00"


def test_failed_target_update_preserves_saved_targets(client, monkeypatch):
    original = client.get("/api/targets").json()
    monkeypatch.setattr(targets_api, "replace_targets", fail_write)

    response = client.put("/api/targets", json={"calories": "1800.00", "protein": "60.00"})

    assert response.status_code == 500
    assert response.json()["error"]["code"] == "persistence_failed"
    assert client.get("/api/targets").json() == original
