from flask import Blueprint, request, jsonify
"""
event_routes.py

This module defines the Flask Blueprint and HTTP routes for event-related operations
in the event management application. It provides endpoints for creating events,
listing upcoming events, registering attendees, and listing attendees for a specific event.

Routes:
    POST   /events                     - Create a new event.
    GET    /events                     - List all upcoming events.
    POST   /events/<event_id>/register - Register an attendee for a specific event.
    GET    /events/<event_id>/attendees- List attendees for a specific event (paginated).

Schemas:
    EventSchema     - Used for serializing and deserializing event data.
    AttendeeSchema  - Used for serializing and deserializing attendee data.

Dependencies:
    - Flask Blueprint, request, jsonify
    - app.services.event_service for business logic
    - app.schemas.event for data validation and serialization
"""
from app.services import event_service
from app.schemas.event import EventSchema, AttendeeSchema

event_bp = Blueprint("event", __name__)
event_schema = EventSchema()
attendee_schema = AttendeeSchema()
attendees_schema = AttendeeSchema(many=True)

@event_bp.route("/events", methods=["POST"])
def create_event():
    """
    ---
    post:
        summary: Create a new event
        description: Creates a new event using the provided JSON data.
        requestBody:
            required: true
            content:
                application/json:
                    schema:
                        $ref: '#/components/schemas/Event'
        responses:
            201:
                description: Event created successfully
                content:
                    application/json:
                        schema:
                            $ref: '#/components/schemas/Event'
            400:
                description: Invalid input data
        tags:
            - Events
    """
    data = event_schema.load(request.json)
    event = event_service.create_event(data)
    return event_schema.dump(event), 201

@event_bp.route("/events", methods=["GET"])
def list_events():
    """
    ---
    get:
        summary: List all upcoming events
        description: Retrieve a list of all upcoming events.
        responses:
            200:
                description: A list of upcoming events
                content:
                    application/json:
                        schema:
                            type: array
                            items:
                                $ref: '#/components/schemas/Event'
        tags:
            - Events
    """
    events = event_service.get_upcoming_events()
    return event_schema.dump(events, many=True)

@event_bp.route("/events/<int:event_id>/register", methods=["POST"])
def register(event_id):
    """
    ---
    post:
        summary: Register an attendee for a specific event
        description: Registers a new attendee for the event with the given event_id.
        parameters:
            - in: path
              name: event_id
              schema:
                type: integer
              required: true
              description: ID of the event to register for
        requestBody:
            required: true
            content:
                application/json:
                    schema:
                        $ref: '#/components/schemas/Attendee'
        responses:
            201:
                description: Attendee registered successfully
                content:
                    application/json:
                        schema:
                            $ref: '#/components/schemas/Attendee'
            400:
                description: Invalid input data
        tags:
            - Attendees
    """
    data = attendee_schema.load(request.json)
    attendee = event_service.register_attendee(event_id, data)
    return attendee_schema.dump(attendee), 201

@event_bp.route("/events/<int:event_id>/attendees", methods=["GET"])
def list_attendees(event_id):
    """
    ---
    get:
        summary: List attendees for a specific event (paginated)
        description: Retrieve a paginated list of attendees for the event with the given event_id.
        parameters:
            - in: path
              name: event_id
              schema:
                type: integer
              required: true
              description: ID of the event to list attendees for
            - in: query
              name: page
              schema:
                type: integer
                default: 1
              required: false
              description: Page number for pagination
            - in: query
              name: per_page
              schema:
                type: integer
                default: 10
              required: false
              description: Number of attendees per page
        responses:
            200:
                description: A paginated list of attendees
                content:
                    application/json:
                        schema:
                            type: object
                            additionalProperties:
                                type: string
            400:
                description: Invalid input data
        tags:
            - Attendees
    """
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    pagination = event_service.get_attendees(event_id, page=page, per_page=per_page)
    d = {}
    for attendee in pagination:
        d[attendee.id] = attendee.name
    return jsonify(d)

