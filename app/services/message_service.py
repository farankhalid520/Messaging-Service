from ..models.message import Message
from .. import db

def create_message(recipient, content):
    """
    Creates and saves new message to the database.
    """
    message = Message(recipient=recipient, content=content)
    db.session.add(message)
    db.session.commit()
    return message

def fetch_messages_by_status(is_read):
    """
    Fetches messages based on read status.
    """
    return Message.query.filter_by(is_read=is_read).order_by(Message.timestamp.asc()).all()

async def update_messages_to_read(messages):
    """
    Asynchronously updates status of messages to read.
    """
    # Updating the status of each message to read
    for message in messages:
        message.is_read = True

    # Committing changes to db
    db.session.commit()


def fetch_messages_by_id_range(start_id, stop_id):
    """
    Fetches messages ordered by timestamp, between start_id and stop_id.
    """
    return Message.query.filter(Message.id >= start_id, Message.id <= stop_id) \
                        .order_by(Message.timestamp.asc()) \
                        .all()



def delete_message(message_id):
    """
    Deletes a specific message by ID.
    """
    message = Message.query.get(message_id)
    if message:
        db.session.delete(message)
        db.session.commit()
        return True
    return False

def delete_messages_in_range(start_id, stop_id):
    """
    Deletes all messages with IDs between start_id and stop_id (inclusive).
    """
    # Filtering messages in specified ID range
    messages_to_delete = Message.query.filter(
        Message.id >= start_id,
        Message.id <= stop_id
    ).all()

    count = len(messages_to_delete)

    # Deleting filtered messages
    if count > 0:
        for message in messages_to_delete:
            db.session.delete(message)
        db.session.commit()

    return count
