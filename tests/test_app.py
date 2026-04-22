from app import app, events, Event
import pytest

@pytest.fixture(autouse=True)
def reset_data():
    # Reset the in-memory "database" before each test
    events.clear()
    events.append(Event(1, "Tech Meetup"))
    events.append(Event(2, "Python Workshop"))

def test_welcome_route():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert response.get_json() == {"message": "Welcome to the Event Management API"}

def test_get_events():
    client = app.test_client()
    response = client.get("/events")
    assert response.status_code == 200
    assert response.get_json() == [
        {"id": 1, "title": "Tech Meetup"},
        {"id": 2, "title": "Python Workshop"},
    ]

def test_create_event():
    client = app.test_client()
    response = client.post("/events", json={"title": "Hackathon"})
    assert response.status_code == 201
    data = response.get_json()
    assert "id" in data and data["title"] == "Hackathon"

def test_create_event_missing_title():
    client = app.test_client()
    response = client.post("/events", json={})
    assert response.status_code == 400

def test_update_event():
    client = app.test_client()
    response = client.patch("/events/1", json={"title": "Hackathon 2025"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["title"] == "Hackathon 2025"

def test_update_event_not_found():
    client = app.test_client()
    response = client.patch("/events/99", json={"title": "Ghost Event"})
    assert response.status_code == 404

def test_delete_event():
    client = app.test_client()
    response = client.delete("/events/2")
    assert response.status_code == 204

def test_delete_event_not_found():
    client = app.test_client()
    response = client.delete("/events/99")
    assert response.status_code == 404
