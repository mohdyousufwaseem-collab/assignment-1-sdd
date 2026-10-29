from datetime import date, timedelta

from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest

from app.api.days import router as days_router
from app.api.meals import router as meals_router
from app.api.targets import router as targets_router
from app.storage.database import initialize_database


def create_test_app():
    application = FastAPI()
    application.include_router(days_router, prefix="/api")
    application.include_router(meals_router, prefix="/api")
    application.include_router(targets_router, prefix="/api")

    @application.on_event("startup")
    def initialize_store():
        initialize_database()

    return application


@pytest.fixture

def configured_environment(tmp_path, monkeypatch):
    monkeypatch.setenv("CALORIE_TRACKER_DATA_DIR", str(tmp_path))
    return tmp_path


def test_first_run_returns_generic_default_targets(configured_environment):
    with TestClient(create_test_app()) as client:
        response = client.get("/api/targets")

    assert response.status_code == 200
    assert response.json() == {"calories": "2000.00", "protein": "50.00"}


def test_target_update_is_used_for_history_and_survives_reopen(configured_environment):
    previous_date = (date.today() - timedelta(days=1)).isoformat()
    meal = {
        "name": "Breakfast",
        "category": "Breakfast",
        "date": previous_date,
        "quantity": "1.00",
        "calories_per_serving": "900.00",
        "protein_per_serving": "30.00",
    }

    with TestClient(create_test_app()) as client:
        assert client.post("/api/meals", json=meal).status_code == 201
        saved = client.put("/api/targets", json={"calories": "1800.00", "protein": "60.00"})
        assert saved.status_code == 200
        day = client.get(f"/api/days/{previous_date}").json()
        assert day["summary"]["calories"]["target"] == "1800.00"
        assert day["summary"]["protein"]["target"] == "60.00"

    with TestClient(create_test_app()) as reopened_client:
        assert reopened_client.get("/api/targets").json() == {
            "calories": "1800.00",
            "protein": "60.00",
        }
