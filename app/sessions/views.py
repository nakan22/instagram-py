from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.sessions.forms import LoginForm
from app.users.models import User
from app import login_manager
from authlib.flask.client import OAuth
from app.helpers import oauth






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
        return redirect(url_for('users.user_profile', id=current_user.id))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('you have been logged in!')
            return redirect(url_for('users.user_profile', id=current_user.id))
        else:
            flash('wrong email/password. try again')
            return redirect(url_for('sessions.login'))
    return render_template('login.html', title='Login', form=form)


@sessions_blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('sessions.home'))
                
@sessions_blueprint.route('/oauth_login', methods=["POST"])
def oauth_login():

    redirect_uri = url_for('sessions.authorize', _external=True)
    print(redirect_uri)
    return oauth.google.authorize_redirect(redirect_uri)
    # return render_template('login.html', title='Login', form=form)

@sessions_blueprint.route('/authorize')
def authorize():
    # token = oauth.google.authorize_access_token()
    # email = oauth.google.get('https://www.googleapis.com/oauth2/v2/userinfo').json()['email']
    # this is a pseudo method, you need to implemenst it yourself
    # OAuth1Token.save(current_user, token, email)
    return redirect(url_for('users.user_profile'))

@sessions_blueprint.route('/profile')
def twitter_profile():
    resp = oauth.google.get('account/verify_credentials.json')
    profile = resp.json()
    return render_template('home.html', profile=profile)

