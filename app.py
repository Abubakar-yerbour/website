# app.py

from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from flask_socketio import SocketIO
from config import Config
from models import db, User
from routes.chat import chat_bp
from routes.admin import admin_bp
from routes.tools import tools_bp

# Initialize Flask app and load config
app = Flask(__name__)
app.config.from_object(Config)

# Initialize database
db.init_app(app)

# Initialize SocketIO
socketio = SocketIO(app)

# Initialize LoginManager
login_manager = LoginManager()
login_manager.login_view = 'login'  # name of the login route function
login_manager.init_app(app)

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Register blueprints
app.register_blueprint(chat_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(tools_bp)

# Main route (login page)
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nickname = request.form.get('nickname')
        password = request.form.get('password')

        user = User.query.filter_by(nickname=nickname).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('chat.general_chat'))
        else:
            return render_template('login.html', error='Invalid credentials')

    return render_template('login.html')

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Run the app
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
