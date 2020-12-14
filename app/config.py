import os


class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECCRET_KEY') or 'admin'
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY") or "admin"
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_ENABLED = True

    MONGODB_SETTINGS = {
        "db": os.environ.get("MONGODB_NAME") or "smanzel_dev",
    }

    MQTT_SETTINGS = {
        "host": "192.168.43.2",
        "port": 8000,
        "useSSL": False
    }


class ProductionConfig(Config):
    MONGODB_SETTINGS = {
        "host": os.environ.get("MONGODB_URI"),
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