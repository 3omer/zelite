from flask import Flask
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from flask_mongoengine import MongoEngine
from app.config import *


app = Flask(__name__)


if app.env == "development":
    app.config.from_object(DevelopmentConfig)
else:
    app.config.from_object(ProductionConfig)

db = MongoEngine(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


from app import routes, auth, mongoDB
from app.API import bot, api, mqtt