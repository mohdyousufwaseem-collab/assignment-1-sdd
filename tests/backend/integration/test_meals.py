from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest

from app.api.days import router as days_router
from app.api.meals import router as meals_router
from app.storage.database import initialize_database


@pytest.fixture

def client(tmp_path, monkeypatch):
    monkeypatch.setenv("CALORIE_TRACKER_DATA_DIR", str(tmp_path))
    application = FastAPI()
    application.include_router(days_router, prefix="/api")
    application.include_router(meals_router, prefix="/api")

    @application.on_event("startup")
    def initialize_store():
        initialize_database()

    with TestClient(application) as test_client:
        yield test_client


def meal_payload(**overrides):
    payload = {
        "name": "  Oatmeal  ",
        "category": "Breakfast",
        "date": "2026-10-28",
        "quantity": "2.50",
        "calories_per_serving": "72.00",
        "protein_per_serving": "6.30",
    }
    payload.update(overrides)
    return payload


def test_create_meal_trims_name_and_returns_persisted_entry(client):
    response = client.post("/api/meals", json=meal_payload())

    assert response.status_code == 201
    assert response.json()["name"] == "Oatmeal"
    assert response.json()["quantity"] == "2.50"


def test_meal_quantity_edit_and_date_move_replaces_old_contribution(client):
    created = client.post("/api/meals", json=meal_payload()).json()
    changed = meal_payload(quantity="3.00", date="2026-10-27")

    response = client.put(f"/api/meals/{created['id']}", json=changed)
    assert response.status_code == 200
    assert response.json()["date"] == "2026-10-27"

    old_day = client.get("/api/days/2026-10-28").json()
    new_day = client.get("/api/days/2026-10-27").json()
    assert old_day["meals"] == []
    assert new_day["summary"]["calories"]["intake"] == "216.00"
    assert new_day["summary"]["protein"]["intake"] == "18.90"


def test_delete_meal_removes_contribution_and_empty_day_state(client):
    created = client.post("/api/meals", json=meal_payload()).json()

    response = client.delete(f"/api/meals/{created['id']}")
    assert response.status_code == 204

    day = client.get("/api/days/2026-10-28").json()
    assert day["has_entries"] is False
    assert day["meals"] == []
    assert day["summary"]["calories"]["intake"] == "0.00"
    assert day["summary"]["protein"]["intake"] == "0.00"


def test_category_choices_are_limited_to_specified_values(client):
    for category in ("Breakfast", "Lunch", "Dinner", "Snack"):
        response = client.post("/api/meals", json=meal_payload(category=category))
        assert response.status_code == 201
        assert response.json()["category"] == category
