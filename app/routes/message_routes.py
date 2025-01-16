from flask import Blueprint
from ..controllers.message import (
    handle_create_message,
    handle_fetch_messages_by_status,
    handle_fetch_all_messages,
    handle_delete_message,
    handle_delete_messages_in_range
)

# Blueprint for message routes
message_bp = Blueprint('message', __name__, url_prefix='/api/v1/messages')

# Defined routes
message_bp.add_url_rule('/send', view_func=handle_create_message, methods=['POST'])
message_bp.add_url_rule('/status', view_func=handle_fetch_messages_by_status, methods=['GET'])
message_bp.add_url_rule('/all', view_func=handle_fetch_all_messages, methods=['GET'])
message_bp.add_url_rule('/delete/<int:message_id>', view_func=handle_delete_message, methods=['DELETE'])
message_bp.add_url_rule('/delete/range', view_func=handle_delete_messages_in_range, methods=['DELETE'])


