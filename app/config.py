import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECCRET_KEY') or 'admin'

    MONGODB_SETTINGS = {
        'db': os.environ.get("MONGO_NAME") or "manzel_v1_test"
    }
