from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.users.models import User



class UserUploads(FlaskForm):
    image = FileField('Upload Images')
    submit = SubmitField('submit')