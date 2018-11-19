from flask import render_template, request
from database import db, app, User


@app.route("/")
def home():
    return render_template('home.html')