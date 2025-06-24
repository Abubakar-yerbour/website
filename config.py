# config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev_secret')
    
    # Use /tmp for writeable space on Render
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
