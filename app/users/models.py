from app import db
from flask_login import UserMixin, current_user
from flask import url_for
from sqlalchemy.ext.hybrid import hybrid_property
from app.config import S3_LOCATION

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(1024), unique=False)
    image_file = db.Column(db.String(1000))
    images = db.relationship("Image", backref='user', lazy=True)
    

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
        # self.image_file = image_file

    @hybrid_property
    def profile_piture_url(self):
        return f"{S3_LOCATION}{self.image_file}"


    # def __repr__(self):
    #     return '<User %r>' % self.username


