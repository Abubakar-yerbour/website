# routes/tools.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, send_from_directory
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from config import Config
import os

tools_bp = Blueprint('tools', __name__)

UPLOAD_FOLDER = os.path.join('static', 'uploads')

@tools_bp.route('/tools', methods=['GET', 'POST'])
@login_required
def tools():
    if request.method == 'POST':
        file = request.files.get('file')
        if file and file.filename:
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            flash("Tool uploaded successfully!", "success")
            return redirect(url_for('tools.tools'))

    files = os.listdir(UPLOAD_FOLDER)
    return render_template('tools.html', files=files)

@tools_bp.route('/uploads/<filename>')
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@tools_bp.route('/tool/<filename>')
def run_tool(filename):
    return render_template('run_tool.html', filename=filename)
