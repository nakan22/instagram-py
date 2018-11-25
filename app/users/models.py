from app import db
from flask_login import UserMixin
from flask import url_for
from sqlalchemy.ext.hybrid import hybrid_property

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(1024), unique=False)
    image_file = db.Column(db.String(1000))
    

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
        # self.image_file = image_file
        

    # def image_url(self):
    #     if self.image_file is None:
    #         image_file = url_for('static', filename='default.jpg')
    #         return image_file
    #     else:
    #         image_file = url_for('static', filename='profile_pics/' + current_user.image + current_user.id)
    #         return image_file

    # def __repr__(self):
    #     return '<User %r>' % self.username
