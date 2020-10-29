import os


class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECCRET_KEY') or 'admin'

    MONGODB_SETTINGS = {
        "db": os.environ.get("MONGODB_NAME") or "smanzel_dev",
    }

    MQTT_SETTINGS = {
        "host": "127.0.0.1",
        "port": 8000,
    }


class ProductionConfig(Config):
    MONGODB_SETTINGS = {
        "host": os.environ.get("MONGODB_URI"),
        "connect": False
    }

    MQTT_SETTINGS = {
        "host": os.environ.get("MQTT_HOST"),
        "port": int(os.environ.get("MQTT_PORT")),
    }

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True