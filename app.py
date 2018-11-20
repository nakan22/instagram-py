from flask import render_template, request, flash, redirect, url_for
from database import db, app, login_manager
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegistrationForm, LoginForm
from flask_login import UserMixin
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
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('you have been logged in!')
            return redirect(url_for('home'))
        else:
            flash('login unsuccessful')
            return redirect(url_for('home'))
    return render_template('login.html', title='Login', form=form)



# @app.route('/<password>')
# def index(password):
#     hashed_value = generate_password_hash(password)

#     result = check_password_hash(stored_password, password)

#     return str(result)

#     return hashed_value

if __name__ == '__main__':
    app.run()
