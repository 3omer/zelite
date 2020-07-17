from flask import jsonify, request, abort
from app import app
from app.mongoDB import Device
from .utils import turn_on, turn_off, get_state
from . import BASE_URL

BOT_API = BASE_URL.format("/bot")


@app.route(BOT_API, methods=["PUT"])
def action():
    """Bot post request to do action
        {
            device: 'light',
            place: 'hall',
            action: 'turn_on'
        }
    """
    d_name = request.args["device"]
    d_place = request.args["place"]
    action = request.args["action"]

    # get the device then filter them by name
    user_devices = Device.get_all()

    if action == "turn_on":
        turn_on(1)
    elif action == "turn_off":
        turn_off(1)
    elif action == "state":
        get_state(id)
