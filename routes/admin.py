# routes/admin.py
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from utils.db import User, db
from utils.decorators import admin_required

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin')
@login_required
@admin_required
def dashboard():
    users = User.query.all()
    return render_template('dashboard.html', users=users)

@admin_bp.route('/admin/reset/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def reset_password(user_id):
    user = User.query.get(user_id)
    new_pass = request.form.get('new_password')
    if user and new_pass:
        user.set_password(new_pass)
        db.session.commit()
        flash(f"Password reset for {user.nickname}.", 'success')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/admin/update/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def update_nickname(user_id):
    user = User.query.get(user_id)
    new_nick = request.form.get('nickname')
    if user and new_nick:
        user.nickname = new_nick
        db.session.commit()
        flash("Nickname updated.", 'success')
    return redirect(url_for('admin.dashboard'))
