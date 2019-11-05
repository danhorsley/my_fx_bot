import os
from flask import Flask, Blueprint
from flask_login import LoginManager 
from flask_sqlalchemy import SQLAlchemy
from decouple import config


APP = Flask(__name__)

APP.config['SECRET_KEY'] = config('DATABASE_URL')#os.environ.get('SECRET_KEY')
#APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
APP.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')#os.environ.get('DATABASE_URL')
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
APP.config['ENV'] = 'debug'
DB = SQLAlchemy(APP)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(APP)

from .models import User

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))

# blueprint for auth routes in our app
from .auth import auth as auth_blueprint
APP.register_blueprint(auth_blueprint)

# blueprint for non-auth parts of app
from .main import main as main_blueprint
APP.register_blueprint(main_blueprint)

from .main import *

if __name__ == '__main__':
    APP.run()