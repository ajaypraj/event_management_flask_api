import pytest
from app.main import create_app
from app.models.event import db as _db
print("Importing test_event.py")
@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        _db.create_all()
        yield app
        _db.session.remove()
        _db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_create_event(client):
    data = {
        "name": "Test Event",
        "location": "Test City",
        "start_time": "2025-07-10T10:00:00",
        "end_time": "2025-07-10T12:00:00",
        "max_capacity": 2
    }
    response = client.post("/events", json=data)
    assert response.status_code == 201
    assert response.json["name"] == "Test Event"

def test_register_attendee(client):
    # Create event first
    event_data = {
        "name": "Test Event",
        "location": "Test City",
        "start_time": "2025-07-10T10:00"}
