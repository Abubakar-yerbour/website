# app.py
from flask import Flask
from config import Config
from utils.db import init_db
from socketio_config import socketio, init_socketio
import os

app = Flask(__name__, instance_relative_config=True)
app.config.from_object(Config)

# Ensure instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

# Initialize extensions
init_socketio(app)
init_db(app)

# Register authentication blueprint
from utils import auth
app.register_blueprint(auth.auth_bp)

# Register other blueprints
from routes import chat, admin, tools
app.register_blueprint(chat.chat_bp)
app.register_blueprint(admin.admin_bp)
app.register_blueprint(tools.tools_bp)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
