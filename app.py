from flask import render_template, request
from database import db, app, User


@app.route('/')
def home():
    print('hello world')
    return render_template('home.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route("/puppies", methods=["POST"])
def create():
    email = request.form.get('name')
    username = request.form.get('username')
    password = request.form.get('password')

    new_user = User(email, username, password)
    
    db.session.add(new_user)
    db.session.commit()

    return render_template('thankyou.html') 



if __name__ == '__main__':
    app.run()
