# routes/chat.py
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from flask_socketio import emit, join_room
from socketio_config import socketio
from utils.db import get_online_users, save_message, get_message_history

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/chat')
@login_required
def general():
    messages = get_message_history(room="general")
    return render_template('chat.html', user=current_user, online_users=get_online_users(), messages=messages)

@socketio.on('join')
def handle_join(data):
    join_room(data['room'])
    emit('user_joined', {'user': data['user']}, room=data['room'])

@socketio.on('send_message')
def handle_send_message(data):
    save_message(sender_id=current_user.id, content=data['content'], room=data['room'])
    emit('receive_message', {
        'sender': current_user.nickname,
        'content': data['content']
    }, room=data['room'])

@socketio.on('tag_user')
def handle_tag_user(data):
    emit('user_tagged', data, room=data['room'])
