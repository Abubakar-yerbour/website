# routes/tools.py

import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, send_from_directory
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from config import Config
from models import db, Tool
from datetime import datetime

tools_bp = Blueprint('tools', __name__)

WEB_TOOL_EXTS = ['.html', '.htm']
WEB_TOOL_DIR = os.path.join("static", "uploads", "webtools")
DOWNLOAD_DIR = os.path.join("static", "uploads", "downloads")

os.makedirs(WEB_TOOL_DIR, exist_ok=True)
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

@tools_bp.route('/tools', methods=['GET', 'POST'])
@login_required
def tools():
    if request.method == 'POST':
        file = request.files.get('file')
        description = request.form.get('description', '')
        
        if file and file.filename:
            filename = secure_filename(file.filename)
            ext = os.path.splitext(filename)[1].lower()

            is_web = ext in WEB_TOOL_EXTS
            subfolder = str(current_user.id) if is_web else ""
            base_dir = WEB_TOOL_DIR if is_web else DOWNLOAD_DIR
            full_dir = os.path.join(base_dir, subfolder)

            os.makedirs(full_dir, exist_ok=True)
            filepath = os.path.join(full_dir, filename)
            file.save(filepath)

            new_tool = Tool(
                uploader_id=current_user.id,
                name=filename,
                filename=filename,
                description=description,
                is_web_tool=is_web,
                filetype=ext,
                created_at=datetime.utcnow()
            )
            db.session.add(new_tool)
            db.session.commit()

            flash("Tool uploaded successfully!", "success")
            return redirect(url_for('tools.tools'))

    all_tools = Tool.query.order_by(Tool.created_at.desc()).all()
    return render_template('tools.html', tools=all_tools, current=current_user)

@tools_bp.route('/tool/<int:tool_id>')
@login_required
def run_tool(tool_id):
    tool = Tool.query.get_or_404(tool_id)

    if not tool.is_web_tool:
        flash("This tool is not web-executable.", "danger")
        return redirect(url_for("tools.tools"))

    tool_path = f"/static/uploads/webtools/{tool.uploader_id}/{tool.filename}"
    return render_template("run_tool.html", tool=tool, path=tool_path)

@tools_bp.route('/download/<int:tool_id>')
@login_required
def download_file(tool_id):
    tool = Tool.query.get_or_404(tool_id)
    if tool.is_web_tool:
        flash("Web tools cannot be downloaded.", "warning")
        return redirect(url_for("tools.tools"))
    
    return send_from_directory(DOWNLOAD_DIR, tool.filename, as_attachment=True)
