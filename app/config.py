import os


class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECCRET_KEY') or 'admin'

    MONGODB_SETTINGS = {
        "db": os.environ.get("MONGODB_NAME") or "smanzel_dev",
    }


class ProductionConfig(Config):
    MONGODB_SETTINGS = {
        "host": os.environ.get("MONGODB_URI"),
        "connect": False
    }

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True