from flask import render_template, request
from database import db, app
from models import Puppy

@app.route("/")
def home():
    return render_template('home.html')