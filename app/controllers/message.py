from flask import jsonify, request
from ..services.message_service import create_message, fetch_messages_by_status, update_messages_to_read, fetch_messages_by_id_range, delete_message, delete_messages_in_range
import asyncio

def handle_create_message():
    """
    Handles creation of new message.
    """
    data = request.get_json()
    recipient = data.get('recipient')
    content = data.get('content')

    if not recipient or not content:
        return jsonify({'error': 'Recipient and content are required'}), 400

    message = create_message(recipient, content)
    return jsonify({
        'id': message.id,
        'recipient': message.recipient,
        'content': message.content,
        'timestamp': message.timestamp.isoformat()
    }), 201


async def handle_fetch_messages_by_status():
    """
    Handles fetching messages based on their status (read or unread),
    and updates the status to read asynchronously if unread messages are fetched.
    """
    # Getting status parameter
    status = request.args.get('status')

    # Validating status parameter
    if status not in ['read', 'unread']:
        return jsonify({'error': 'Status must be "read" or "unread"'}), 400

    # Fetching messages based on status
    is_read = status == 'read'
    messages = fetch_messages_by_status(is_read)

    # Updating status to read asynchronously for unfetched messages
    if not is_read:
        asyncio.create_task(update_messages_to_read(messages))

    # Returning messages in JSON 
    return jsonify([{
        'id': m.id,
        'recipient': m.recipient,
        'content': m.content,
        'timestamp': m.timestamp.isoformat(),
        'is_read': m.is_read
    } for m in messages])


def handle_fetch_all_messages():
    """
    Handles fetching all messages (including previously fetched) ordered by time and by start and stop message ids.
    """
    # Getting start and stop id parameters
    start_id = int(request.args.get('start', 1))  # Default to 1 
    stop_id = int(request.args.get('stop', 10))   # Default to 10 

    # Fetching messages ordered by timestamp
    messages = fetch_messages_by_id_range(start_id, stop_id)

    # Returning messages in JSON
    return jsonify([{
        'id': m.id,
        'recipient': m.recipient,
        'content': m.content,
        'timestamp': m.timestamp.isoformat(),
        'is_read': m.is_read
    } for m in messages])


def handle_delete_message(message_id):
    """
    Handles deletion of specific message.
    """
    if delete_message(message_id):
        return jsonify({'message': 'Message deleted successfully'}), 200
    return jsonify({'error': 'Message not found'}), 404


def handle_delete_messages_in_range():
    """
    Deletes all messages between start_id and stop_id (inclusive).
    """

    start_id = request.args.get('start_id')
    stop_id = request.args.get('stop_id')

    # Validating input
    if not start_id or not stop_id:
        return jsonify({'error': 'Both start_id and stop_id are required'}), 400

    try:
        start_id = int(start_id)
        stop_id = int(stop_id)
    except ValueError:
        return jsonify({'error': 'start_id and stop_id must be integers'}), 400

    deleted_count = delete_messages_in_range(start_id, stop_id)

    return jsonify({
        'message': f'{deleted_count} messages deleted between IDs {start_id} and {stop_id}'
    }), 200
