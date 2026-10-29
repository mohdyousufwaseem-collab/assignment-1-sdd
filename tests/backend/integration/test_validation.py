from datetime import date

from fastapi.testclient import TestClient
import pytest

from app.main import app
from app.storage.database import initialize_database


def meal_payload(**overrides):
    payload = {
        "name": "Oatmeal",
        "category": "Breakfast",
        "date": date.today().isoformat(),
        "quantity": "1.00",
        "calories_per_serving": "250.00",
        "protein_per_serving": "10.00",
    }
    payload.update(overrides)
    return payload


@pytest.fixture

def client(tmp_path, monkeypatch):
    monkeypatch.setenv("CALORIE_TRACKER_DATA_DIR", str(tmp_path))
    with TestClient(app, base_url="http://127.0.0.1") as test_client:
        yield test_client


@pytest.mark.parametrize("value", [" ", "x" * 81])
def test_invalid_trimmed_name_is_rejected(client, value):
    response = client.post("/api/meals", json=meal_payload(name=value))

    assert response.status_code == 422
    assert response.json()["error"]["code"] == "validation_failed"
    assert "name" in response.json()["error"]["fields"]


@pytest.mark.parametrize("value", ["0", "100.01", "-1", "+1", "1,000", "1e2", "1.001", "abc"])
def test_invalid_quantity_is_rejected(client, value):
    response = client.post("/api/meals", json=meal_payload(quantity=value))

    assert response.status_code == 422
    assert "quantity" in response.json()["error"]["fields"]


@pytest.mark.parametrize(
    ("field", "invalid"),
    [
        ("calories_per_serving", "-1"),
        ("calories_per_serving", "10000.01"),
        ("calories_per_serving", "1e3"),
        ("calories_per_serving", "1.001"),
        ("protein_per_serving", "-1"),
        ("protein_per_serving", "1000.01"),
        ("protein_per_serving", "+1"),
        ("protein_per_serving", "1,000"),
        ("protein_per_serving", "1.001"),
    ],
)
def test_invalid_nutrition_value_is_rejected(client, field, invalid):
    response = client.post("/api/meals", json=meal_payload(**{field: invalid}))

    assert response.status_code == 422
    assert field in response.json()["error"]["fields"]


@pytest.mark.parametrize(
    ("value", "expected"),
    [("1.00", 200), ("100000.00", 200), ("0", 422), ("100000.01", 422), ("-1", 422), ("1e3", 422), ("1.001", 422)],
)
def test_calorie_target_boundaries(client, value, expected):
    response = client.put("/api/targets", json={"calories": value, "protein": "50.00"})

    assert response.status_code == expected


@pytest.mark.parametrize(
    ("value", "expected"),
    [("0.01", 200), ("10000.00", 200), ("0", 422), ("10000.01", 422), ("-1", 422), ("+1", 422), ("1.001", 422)],
)
def test_protein_target_boundaries(client, value, expected):
    response = client.put("/api/targets", json={"calories": "2000.00", "protein": value})

    assert response.status_code == expected


@pytest.mark.parametrize("invalid_date", ["2026-02-30", "not-a-date", "2026-1-01"])
def test_invalid_calendar_date_is_rejected(client, invalid_date):
    response = client.post("/api/meals", json=meal_payload(date=invalid_date))

    assert response.status_code == 422
    assert "date" in response.json()["error"]["fields"]


def test_future_date_and_category_are_rejected(client):
    future_date = date.fromordinal(date.today().toordinal() + 1).isoformat()
    future_response = client.post("/api/meals", json=meal_payload(date=future_date))
    category_response = client.post("/api/meals", json=meal_payload(category="Brunch"))

    assert future_response.status_code == 422
    assert "date" in future_response.json()["error"]["fields"]
    assert category_response.status_code == 422
    assert "category" in category_response.json()["error"]["fields"]
