from functools import wraps
from flask import request, abort, g, jsonify
from app.mongoDB import Hub

def turn_on(id):
    pass

def turn_off(id):
    pass

def get_state(id):
    pass

def doesnt_exist(port=''):
    abort(404)


def token_required(view):
    """Inject apikey from header X-Api-Key into the global object 'g' as token
    @:param view: flask view function
    @:return: flask view
    """
    @wraps(view)
    def decorated_view(*args, **kwargs):
        key = request.headers.get("x-api-key")
        if key:
            g.token = key
            return view(*args, **kwargs)
        else:
            return jsonify(error="Unauthorized"), 401
    return decorated_view


