# app.py
from flask import Flask
from flask_socketio import SocketIO
from utils.db import init_db
from config import Config
import os
import eventlet

app = Flask(__name__, instance_relative_config=True)
app.config.from_object(Config)

socketio = SocketIO(app, async_mode='eventlet')

# Ensure instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

# Import routes
from utils import auth
app.register_blueprint(auth.auth_bp)

from routes import chat, admin, tools
app.register_blueprint(chat.chat_bp)
app.register_blueprint(admin.admin_bp)
app.register_blueprint(tools.tools_bp)

# Initialize DB
init_db()

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
