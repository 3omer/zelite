import os
from datetime import timedelta


class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'admin'
    JWT_SECRET_KEY = "admin"
    JWT_BLACKLIST_ENABLED = True
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=15)

    MONGODB_SETTINGS = {
        "host": os.environ.get("MONGODB_URL")
    }

    MQTT_SETTINGS = {
        "host": os.environ.get("MQTT_HOST") or '127.0.0.1',
        "port": os.environ.get("MQTT_PORT") or 1883,
        "useSSL": os.environ.get("MQTT_USE_SSL", ) == '1'
    }

    # FLASK-MAIL config
    SEND_EMAIL = os.environ.get("SEND_EMAIL", "0") == "1"
    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", "587"))
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", '0') == '1'
    MAIL_USE_SSL = os.environ.get("MAIL_USE_SSL", '0') == '1'


class ProductionConfig(Config):
    MONGODB_SETTINGS = {
        "host": os.environ.get("MONGODB_URL"),
        "connect": False
    }

    MQTT_SETTINGS = {
        "host": os.environ.get("MQTT_HOST"),
        "port": int(os.environ.get("MQTT_PORT") or 8081),
        "useSSL": os.environ.get("MQTT_SSL", "0") == "1"
    }


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
