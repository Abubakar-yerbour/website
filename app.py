from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from flask_socketio import SocketIO
from werkzeug.security import check_password_hash, generate_password_hash
from config import Config
from models import db, User

# Import blueprints
from routes.chat import chat_bp
from routes.admin import admin_bp
from routes.tools import tools_bp
from routes.user import user_bp  # ✅ Added user settings

# Initialize app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
socketio = SocketIO(app, async_mode="threading")
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Register blueprints
app.register_blueprint(chat_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(tools_bp)
app.register_blueprint(user_bp)  # ✅ Register user blueprint

# User loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Route: Login
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        nickname = request.form["nickname"]
        password = request.form["password"]
        user = User.query.filter_by(nickname=nickname).first()
        if user and check_password_hash(user.password, password):
            user.online = True
            db.session.commit()
            login_user(user)
            return redirect(url_for("chat.general"))
        else:
            return render_template("login.html", error="Invalid credentials.")
    return render_template("login.html")

# Route: Logout
@app.route("/logout")
@login_required
def logout():
    current_user.online = False
    db.session.commit()
    logout_user()
    return redirect(url_for("login"))

# Run the app
if __name__ == "__main__":
    with app.app_context():
        db.create_all()

        # Create default admin user if not exists
        if not User.query.filter_by(nickname="admin").first():
            hashed_pw = generate_password_hash("admin")
            admin = User(nickname="admin", password=hashed_pw, is_admin=True, online=False)
            db.session.add(admin)
            db.session.commit()
            print("✅ Tables created and default admin added.")
        else:
            print("✅ Tables already exist. Skipping creation.")

    socketio.run(app, host="0.0.0.0", port=10000, allow_unsafe_werkzeug=True)
