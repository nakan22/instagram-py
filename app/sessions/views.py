from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.sessions.forms import LoginForm
from app.users.models import User
from app import login_manager




sessions_blueprint = Blueprint('sessions', __name__)




@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@sessions_blueprint.route('/')
def home():
    print('hello world')
    return render_template('home.html')


@sessions_blueprint.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('sessions.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('you have been logged in!')
            return redirect(url_for('sessions.home'))
        else:
            flash('wrong email/password. try again')
            return redirect(url_for('sessions.login'))
    return render_template('login.html', title='Login', form=form)


@sessions_blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('sessions.home'))

