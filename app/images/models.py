from app import db
from flask_login import UserMixin, current_user
from flask import url_for
from sqlalchemy.ext.hybrid import hybrid_property
from app.config import S3_LOCATION
from app.users.models import User


class Image(UserMixin, db.Model):
    __tablename__ ='image'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    image_name = db.Column(db.String)
    donations = db.relationship("Donation", backref='image')


    def __init__(self, user_id, image_name):
        self.user_id = user_id
        self.image_name = image_name
    
    @hybrid_property
    def image_url(self):
        return f"{S3_LOCATION}{self.image_name}"



class Donation(UserMixin, db.Model):
    __tablename__ ='donation'

    transaction_id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Numeric(), nullable=False)
    image_id = db.Column(db.Integer, db.ForeignKey('image.id'))

    def __init__(self, amount):
        self.amount = amount

