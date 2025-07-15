from flask import Flask
from app.models.event import db
from app.routes.event_routes import event_bp
from flasgger import Swagger
def create_app():
    app = Flask(__name__)
    swagger = Swagger(app)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///events.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    app.register_blueprint(event_bp)
    with app.app_context():
        db.create_all()
    return app
