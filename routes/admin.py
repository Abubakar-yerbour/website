# routes/admin.py
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from models import db, User
from utils.decorators import admin_required

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin')
@login_required
@admin_required
def dashboard():
    users = User.query.all()
    return render_template("dashboard.html", users=users, current=current_user)

# Create user (admin only)
@admin_bp.route('/admin/create', methods=['POST'])
@login_required
@admin_required
def create_user():
    nickname = request.form.get("nickname")
    password = request.form.get("password")
    if nickname and password:
        if User.query.filter_by(nickname=nickname).first():
            flash("User with that nickname already exists.", "danger")
        else:
            new_user = User(
                nickname=nickname,
                password=generate_password_hash(password),
                is_admin=False
            )
            db.session.add(new_user)
            db.session.commit()
            flash(f"User @{nickname} created.", "success")
    else:
        flash("Missing nickname or password.", "danger")
    return redirect(url_for("admin.dashboard"))

# Admin resets any user password
@admin_bp.route('/admin/reset/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def reset_password(user_id):
    user = User.query.get(user_id)
    new_pass = request.form.get('new_password')
    if user and new_pass:
        user.password = generate_password_hash(new_pass)
        db.session.commit()
        flash(f"Password reset for @{user.nickname}.", 'success')
    return redirect(url_for('admin.dashboard'))

# Admin updates nickname of any user
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

# Admin updates own nickname/password
@admin_bp.route('/admin/settings', methods=["GET", "POST"])
@login_required
@admin_required
def admin_settings():
    if request.method == "POST":
        new_nick = request.form.get("nickname")
        new_pass = request.form.get("password")

        if new_nick:
            current_user.nickname = new_nick
        if new_pass:
            current_user.password = generate_password_hash(new_pass)
        db.session.commit()
        flash("Settings updated.", "success")
        return redirect(url_for("admin.admin_settings"))

    return render_template("admin_settings.html", current=current_user)
