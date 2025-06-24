# routes/chat.py
from flask import Blueprint, render_template, session, redirect, url_for
from flask_login import login_required, current_user
from utils.db import get_online_users
from flask_socketio import emit, join_room
from app import socketio

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/chat')
@login_required
def chat():
    return render_template('chat.html', user=current_user, online_users=get_online_users())

@socketio.on('join')
def handle_join(data):
    join_room(data['room'])
    emit('user_joined', {'user': data['user']}, room=data['room'])

@socketio.on('send_message')
def handle_send_message(data):
    emit('receive_message', data, room=data['room'])

@socketio.on('tag_user')
def handle_tag_user(data):
    emit('user_tagged', data, room=data['room'])
