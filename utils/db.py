# utils/db.py
from models import db, User, Message
from datetime import datetime


def get_online_users():
    return User.query.filter_by(online=True).all()


def save_message(sender_id, content, room='general'):
    message = Message(sender_id=sender_id, content=content, room=room, timestamp=datetime.utcnow())
    db.session.add(message)
    db.session.commit()


def get_message_history(room='general', limit=100):
    return Message.query.filter_by(room=room).order_by(Message.timestamp.asc()).limit(limit).all()
    
