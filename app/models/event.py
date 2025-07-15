from flask_sqlalchemy import SQLAlchemy
"""
This module defines the SQLAlchemy models for the event management application.

Classes:
    Event: Represents an event with attributes such as name, location, start and end times, and maximum capacity.
        - attendees: Relationship to the Attendee model, allowing access to all attendees of an event.
            # Line 15: The 'attendees' relationship establishes a one-to-many link between Event and Attendee.
            # It enables querying all attendees for a given event and ensures that deleting an event
            # will also delete all associated attendees due to the 'cascade="all, delete"' option.

    Attendee: Represents an attendee registered for an event, with a unique constraint on (event_id, email)
        to prevent duplicate registrations for the same event.
"""
from datetime import datetime

db = SQLAlchemy()

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    max_capacity = db.Column(db.Integer, nullable=False)

    attendees = db.relationship("Attendee", backref="event", cascade="all, delete")

class Attendee(db.Model):
    __tablename__ = 'attendees'
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)

    __table_args__ = (
        db.UniqueConstraint('event_id', 'email', name='_event_email_uc'),
    )
