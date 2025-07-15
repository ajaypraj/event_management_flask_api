# Flask Event Management API

## Setup

```bash
pip install -r requirements.txt
python run.py
```

## API Endpoints

- `POST /events` - Create an event
- `GET /events` - List all events
- `POST /events/<event_id>/register` - Register an attendee
- `GET /events/<event_id>/attendees?page=1` - List attendees (pagination)
