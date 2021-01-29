import os
from datetime import timedelta

class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECCRET_KEY') or 'admin'
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY") or "admin"
    JWT_BLACKLIST_ENABLED = True
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=15)

    MONGODB_SETTINGS = {
        "host": os.environ.get("MONGODB_URL"),
        "db": os.environ.get("MONGODB_NAME") or "zelite_dev",
    }

    MQTT_SETTINGS = {
        "host": os.environ.get("MQTT_HOST"),
        "port": os.environ.get("MQTT_PORT"),
        "useSSL": os.environ.get("MQTT_USE_SSL") or False
    }


class ProductionConfig(Config):
    MONGODB_SETTINGS = {
        "host": os.environ.get("MONGODB_URL"),
        "connect": False
    }

    MQTT_SETTINGS = {
        "host": os.environ.get("MQTT_HOST"),
        "port": int(os.environ.get("MQTT_PORT") or 8081),
        "useSSL": os.environ.get("MQTT_SSL") or True
    }

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True