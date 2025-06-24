# utils/auth.py
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash
from utils.db import db
from utils.models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nickname = request.form['nickname']
        password = request.form['password']
        user = User.query.filter_by(nickname=nickname).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['nickname'] = user.nickname
            session['is_admin'] = user.is_admin
            user.online = True
            db.session.commit()
            return redirect(url_for('admin.dashboard' if user.is_admin else 'chat.general_chat'))
        else:
            flash('Invalid nickname or password', 'danger')
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    from utils.models import User
    uid = session.get('user_id')
    if uid:
        user = User.query.get(uid)
        if user:
            user.online = False
            db.session.commit()
    session.clear()
    return redirect(url_for('auth.login'))
