# utils/db.py

from models import User  # ✅ Use User and db from your existing models.py

def get_online_users():
    return User.query.filter_by(online=True).all()
