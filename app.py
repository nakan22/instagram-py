from flask import render_template, request
from database import db, app, User


@app.route('/')
def home():
    print('hello world')
    return render_template('home.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')




if __name__ == '__main__':
    app.run()
