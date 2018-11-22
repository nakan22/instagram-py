from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(1024), unique=False)
    image_file = db.Column(db.String(50), nullable=False, default= 'default.jpg')
    

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password


    # def __repr__(self):
    #     return '<User %r>' % self.username
