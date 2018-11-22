from flask import render_template, request, flash, redirect, url_for
from database import db, app, login_manager
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegistrationForm, LoginForm, EditForm
from flask_login import login_required, login_user, logout_user, current_user
# app.config['SECRET_KEY'] = 'cc883108399d3ddb3186679bbd56c136'

app.config.update(dict(
    SECRET_KEY="cc883108399d3ddb3186679bbd56c136"
    
))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    print('hello world')
    return render_template('home.html')


@app.route('/signup', methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'{form.username.data}, your account has been created, you can now log in!')
        return redirect(url_for('login'))
    return render_template('signup.html', title='Register', form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('you have been logged in!')
            return redirect(url_for('home'))
        else:
            flash('wrong email/password. try again')
            return redirect(url_for('login'))
    return render_template('login.html', title='Login', form=form)

@app.route('/edit/<id>', methods=["GET", "POST"])
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
        return redirect(url_for('login'))        
        
    return render_template('edit.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))



if __name__ == '__main__':
    app.run()