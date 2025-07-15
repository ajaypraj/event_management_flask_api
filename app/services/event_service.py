from flask import abort
from app.models.event import db, Event, Attendee

def create_event(data):
    event = Event(**data)
    db.session.add(event)
    db.session.commit()
    return event

def get_upcoming_events():
    return Event.query.all()

def register_attendee(event_id, data):
    event = Event.query.get(event_id)
    if not event:
        abort(404, "Event not found")
    if len(event.attendees) >= event.max_capacity:
        abort(400, "Event is full")
    if Attendee.query.filter_by(event_id=event_id, email=data['email']).first():
        abort(400, "Attendee already registered")
    attendee = Attendee(event_id=event_id, **data)
    db.session.add(attendee)
    db.session.commit()
    return attendee

def get_attendees(event_id, page=1, per_page=10):
    return Attendee.query.filter_by(event_id=event_id).paginate(page=page, per_page=per_page).items
