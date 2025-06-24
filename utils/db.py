# utils/db.py
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

db = SQLAlchemy()

def init_db(app=None):
    from utils.models import User, Folder, Message, Tool

    if app is not None:
        db.init_app(app)
        with app.app_context():
            db.create_all()

            # Create default admin if not exists
            if not User.query.filter_by(nickname='admin').first():
                admin = User(
                    nickname='admin',
                    password=generate_password_hash('admin'),
                    is_admin=True
                )
                db.session.add(admin)
                db.session.commit()

def get_online_users():
    from utils.models import User
    return User.query.filter_by(online=True).all()
