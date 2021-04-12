from flask import Flask
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from flask_mongoengine import MongoEngine
from flask_cors import CORS
from flask_mail import Mail
from app.config import *


app = Flask(__name__)

if app.env == "development":
    app.config.from_object(DevelopmentConfig)
else:
    app.config.from_object(ProductionConfig)

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

db = MongoEngine(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
jwt_manager = JWTManager(app)
mail = Mail(app)


from app import models
from app.API import bot, devices, mqtt, authAPI