from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.users.forms import RegistrationForm, EditForm
from app.users.models import User
from app import db



users_blueprint = Blueprint('users', __name__)



@users_blueprint.route('/signup', methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('sessions.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'{form.username.data}, your account has been created, you can now log in!')
        return redirect(url_for('sessions.login'))
    return render_template('signup.html', title='Register', form=form)

@users_blueprint.route('/edit/<id>', methods=["GET", "POST"])
@login_required
def edit(id):
    form = EditForm()
    user = User.query.get(id)
    if form.validate_on_submit():
        user.password = generate_password_hash(form.password.data)
        user.email = form.email.data
        db.session.add(user)
        db.session.commit()
        flash(f'{user.username}, your account has been updated, you can now log in!')
        return redirect(url_for('sessions.login'))        
        
    return render_template('edit.html', form=form)
