# utils/tool_handler.py
import os
import zipfile
from flask import current_app
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'zip', 'html', 'htm', 'css', 'js', 'py'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_tool_upload(file, tool_name):
    folder_path = os.path.join(current_app.config['UPLOAD_FOLDER'], secure_filename(tool_name))
    os.makedirs(folder_path, exist_ok=True)

    filename = secure_filename(file.filename)
    file_path = os.path.join(folder_path, filename)
    file.save(file_path)

    # If it's a zip file, extract it
    if filename.endswith('.zip'):
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(folder_path)
        os.remove(file_path)  # remove zip after extraction

    return os.path.relpath(folder_path, start='static')

def list_uploaded_tools():
    upload_root = os.path.join('static', 'uploads')
    return [f for f in os.listdir(upload_root) if os.path.isdir(os.path.join(upload_root, f))]
