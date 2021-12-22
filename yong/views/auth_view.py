from flask import Blueprint, render_template, redirect, url_for, flash, request
from ..forms import RegistrationForm, LoginForm
from flask_login import login_user, logout_user, login_required
from yong.models.user_model import User
from bcrypt import hashpw, gensalt, checkpw


bp = Blueprint('auth', __name__, url_prefix='/')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate_on_submit():
        name = request.form['name']
        email = request.form['email']
        pw = request.form['pw']
        pw_hash = hashpw(pw.encode('UTF-8'), gensalt()).decode()
        if not User.find(email):
            try:
                User.create(name, email, pw_hash)
            except:
                None
            User.create(name, email, pw_hash)
            user = User.find(email)
            login_user(user)
            return redirect(url_for('main.home'))
        else:
            error = '이미 존재하는 이메일입니다.'
        flash(error)
    return render_template('auth/register.html', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        error = None
        input_email = request.form['email']
        input_pw = request.form['pw']
        if not User.find(input_email):
            error = '존재하지 않는 사용자입니다.'
        elif not checkpw(input_pw.encode('UTF-8'), User.find(input_email).user_pw.encode('UTF-8')):
            error = '비밀번호가 일치하지 않습니다.'
        if error is None:
            user = User.find(input_email)
            login_user(user)
            return redirect(url_for('main.home'))
        flash(error)
    return render_template('auth/login.html', form=form)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))