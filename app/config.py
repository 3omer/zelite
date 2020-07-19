import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECCRET_KEY') or 'admin'

    MONGODB_SETTINGS = {
        "db": os.environ.get("MONGODB_NAME") or "manzel_v1_test",
        "host": os.environ.get("MONGODB_URI"),
        "connect": False
    }

class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECCRET_KEY') or 'admin'

    MONGODB_SETTINGS = {
        "db": os.environ.get("MONGODB_NAME") or "manzel_v1_test",
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