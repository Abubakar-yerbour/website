# utils/db.py
from models import User  # ✅ This is now the only valid User model

def get_online_users():
    return User.query.filter_by(online=True).all()
