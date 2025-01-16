from flask import Flask
from .message_routes import message_bp

def register_routes(app: Flask):
    """
    Register all route blueprints.
    """
    app.register_blueprint(message_bp)
