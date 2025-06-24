# config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'unknown-gods-secret-key'
    UPLOAD_FOLDER = os.path.join('static', 'uploads')
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB max file size
    SQLALCHEMY_DATABASE_URI = 'sqlite:///instance/chat.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
