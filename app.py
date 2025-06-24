from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from flask_socketio import SocketIO
from config import Config
from models import db, User  # ✅ Correct import

# Import blueprints
from routes.chat import chat_bp
from routes.admin import admin_bp
from routes.tools import tools_bp

# Initialize app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
socketio = SocketIO(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Register blueprints
app.register_blueprint(chat_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(tools_bp)

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
        if user and user.password == password:
            login_user(user)
            return redirect(url_for("chat.general"))
        else:
            return render_template("login.html", error="Invalid credentials.")
    return render_template("login.html")

# Route: Logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

# Run the app
if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=10000)
