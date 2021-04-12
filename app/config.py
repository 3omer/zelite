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
        "host": os.environ.get("MQTT_HOST") or '127.0.0.1',
        "port": os.environ.get("MQTT_PORT") or 1883,
        "useSSL": os.environ.get("MQTT_USE_SSL") or False
    }

    # FLASK-MAIL config
    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", "587"))
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_USE_TLS = int(os.environ.get("MAIL_USE_TLS", True))
    MAIL_USE_SSL = int(os.environ.get("MAIL_USE_SSL", False))


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
