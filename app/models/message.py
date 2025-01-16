from .. import db
from datetime import datetime

class Message(db.Model):
    """
    Message Model:
    Represents a plain-text message sent to a recipient.

    Attributes:
        id (int): Unique ID for the message.
        recipient (str): Identifier for the recipient.
        content (str): Plain text content of the message.
        is_read (bool): Read status of the message.
        timestamp (datetime): Time the message was created.
    """
    id = db.Column(db.Integer, primary_key=True)
    recipient = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Message(id={self.id}, recipient='{self.recipient}', is_read={self.is_read})>"
