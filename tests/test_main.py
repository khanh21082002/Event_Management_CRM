import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_all_users():
    response = client.get("/users/all")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_user():
    data = {
        "firstName": "Unit",
        "lastName": "Test",
        "email": "unit.test@example.com"
    }
    response = client.post("/users", json=data)
    assert response.status_code == 200
    assert response.json()["email"] == data["email"]

def test_filter_users():
    response = client.get("/users?company=ABC")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_event():
    data = {
        "slug": "unit-test-event",
        "title": "Unit Test Event",
        "startAt": "2023-10-01T10:00:00Z",
        "endAt": "2023-10-01T12:00:00Z",
        "maxCapacity": 100,
        "owner": "unit_test_owner"
    }
    response = client.post("/events", json=data)
    assert response.status_code == 200
    assert response.json()["title"] == data["title"]

def test_list_events():
    response = client.get("/events")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

    

