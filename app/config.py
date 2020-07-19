import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECCRET_KEY') or 'admin'

    MONGODB_SETTINGS = {
        "db": os.environ.get("MONGODB_NAME") or "manzel_v1_test",
        "host": os.environ.get("MONGODB_URI"),
        "connect": False
    }
