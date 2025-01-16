from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    # Initializing db with app
    db.init_app(app)

    # Initializing Flask-Migrate
    migrate = Migrate(app, db)

    # Registering routes
    with app.app_context():
        from .routes import register_routes
        register_routes(app)

    return app
