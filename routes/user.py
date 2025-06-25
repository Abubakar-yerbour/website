# routes/user.py
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from models import db

user_bp = Blueprint('user', __name__)

@user_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def user_settings():
    if current_user.is_admin:
        return redirect(url_for('admin.admin_settings'))

    if request.method == 'POST':
        new_password = request.form.get('password')
        if new_password:
            current_user.password = generate_password_hash(new_password)
            db.session.commit()
            flash("Password updated successfully.", "success")
        else:
            flash("Password cannot be empty.", "danger")

        return redirect(url_for('user.user_settings'))

    return render_template('user/settings.html', user=current_user)
