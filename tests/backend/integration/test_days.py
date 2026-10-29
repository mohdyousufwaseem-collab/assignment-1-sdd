from datetime import date, timedelta

from fastapi.testclient import TestClient
import pytest

from app.main import app


def meal_payload(entry_date: str, name: str, calories: str, protein: str):
    return {
        "name": name,
        "category": "Lunch",
        "date": entry_date,
        "quantity": "1.00",
        "calories_per_serving": calories,
        "protein_per_serving": protein,
    }


@pytest.fixture

def client(tmp_path, monkeypatch):
    monkeypatch.setenv("CALORIE_TRACKER_DATA_DIR", str(tmp_path))
    with TestClient(app, base_url="http://127.0.0.1") as test_client:
        yield test_client


def test_day_endpoint_isolates_meals_by_local_calendar_date(client):
    today = date.today()
    yesterday = (today - timedelta(days=1)).isoformat()
    today_text = today.isoformat()
    assert client.post("/api/meals", json=meal_payload(yesterday, "Yesterday", "300.00", "12.00")).status_code == 201
    assert client.post("/api/meals", json=meal_payload(today_text, "Today", "450.00", "18.00")).status_code == 201

    previous_day = client.get(f"/api/days/{yesterday}").json()
    current_day = client.get(f"/api/days/{today_text}").json()

    assert [meal["name"] for meal in previous_day["meals"]] == ["Yesterday"]
    assert previous_day["summary"]["calories"]["intake"] == "300.00"
    assert [meal["name"] for meal in current_day["meals"]] == ["Today"]
    assert current_day["summary"]["protein"]["intake"] == "18.00"


def test_empty_historical_day_has_current_targets_and_remaining_values(client):
    empty_date = (date.today() - timedelta(days=2)).isoformat()
    day = client.get(f"/api/days/{empty_date}").json()

    assert day["has_entries"] is False
    assert day["meals"] == []
    assert day["summary"]["calories"] == {
        "intake": "0.00", "target": "2000.00", "remaining": "2000.00",
        "excess": "0.00", "progress_percent": "0.0",
    }
    assert day["summary"]["protein"] == {
        "intake": "0.00", "target": "50.00", "remaining": "50.00",
        "excess": "0.00", "progress_percent": "0.0",
    }


def test_day_endpoint_rejects_future_dates(client):
    future_date = (date.today() + timedelta(days=1)).isoformat()
    response = client.get(f"/api/days/{future_date}")

    assert response.status_code == 422
    assert response.json()["error"]["code"] == "validation_failed"
    assert "date" in response.json()["error"]["fields"]
