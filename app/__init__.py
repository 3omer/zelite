from flask import Flask
from flask_login import LoginManager
from app.config import *
from flask_mongoengine import MongoEngine


app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
db = MongoEngine(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from app import routes, auth, mongoDB
from app.API import bot, hub, api