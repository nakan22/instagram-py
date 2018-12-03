import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from app.helpers import oauth
import app.config
from flask_assets import Bundle, Environment

js = Bundle('js/bootstrap.min.js', 'js/popper.min.js', 'js/jquery.min.js', output='gen/main.js')



# This grabs our directory
basedir = os.path.abspath(os.path.dirname(__file__))



app = Flask(__name__)
oauth.init_app(app)
app.config.from_object(os.environ['APP_SETTINGS'])

assets = Environment(app)
assets.register('main_js', js)

# Connects our Flask App to our Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://next:nextacademy@localhost/insta'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'cc883108399d3ddb3186679bbd56c136'


db = SQLAlchemy(app)


login_manager = LoginManager(app)
login_manager.login_view = 'sessions.login'


from app.users.views import users_blueprint
from app.sessions.views import sessions_blueprint

app.register_blueprint(users_blueprint)
app.register_blueprint(sessions_blueprint)


# Add on migration capabilities in order to run terminal commands
Migrate(app,db)



