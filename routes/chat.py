# routes/chat.py
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from flask_socketio import emit, join_room
from models import db, Message
from utils.db import get_online_users

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/chat')
@login_required
def general():
    messages = Message.query.order_by(Message.timestamp).all()
    return render_template('chat.html', user=current_user, online_users=get_online_users(), messages=messages)

@socketio.on('join')
def handle_join(data):
    join_room(data['room'])
    emit('user_joined', {'user': data['user']}, room=data['room'])

@socketio.on('send_message')
def handle_send_message(data):
    content = data.get('content')
    room = data.get('room', 'general')
    if content:
        msg = Message(sender_id=current_user.id, content=content, room=room)
        db.session.add(msg)
        db.session.commit()
        emit('receive_message', {
            'user': current_user.nickname,
            'content': content
        }, room=room)

@socketio.on('tag_user')
def handle_tag_user(data):
    emit('user_tagged', data, room=data['room'])
