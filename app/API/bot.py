from flask import jsonify, request, abort
from app import app
from app.mongoDB import Device, User, Hub
from .utils import turn_on, turn_off, get_state
from . import BASE_URL

BOT_API = BASE_URL.format("/bot")


@app.route(BOT_API, methods=["PUT"])
def action():
    """ PUT request to do action
        {
            device: 'light',
            place: 'hall',
            action: 'turn_on'
        }

        if target device not found return suggestions with devices have similar name/ devices in same place

        if action is to read :
        currently supported sensors : temperature
        request temperature:
        {
        device: 'temperature'
        place: 'room1',
        action: 'read'
        }
    """

    data = request.get_json()
    try:
        name = data.get("name")
        place = data.get("place")
        action = data.get("action")
    except Exception as e:
        return jsonify({"error": "Provide a name, a place and an action."}), 400

    # get the device then filter them by name
    user = User.objects().first() # this is just for testing
    hubs = Hub.by_owner(user)

    target_hub = None
    target_device = None

    for hub in hubs:
        target_device = hub.devices.filter(name=name, place=place).first()
        if target_device:
            target_hub = hub
            break

    if not target_device:
        return jsonify({"error": "Not found"}), 404

    if action == "read":
        return jsonify({"data": target_device.value})

    try:
        if action == "turn_on":
            target_device.is_on = True
        elif action == "turn_off":
            target_device.is_on = False
        else:
            raise Exception("Unknown Action")

        target_hub.save()
        return jsonify({"data": "success"}), 200
    except:
        return jsonify({"error": "Unknown Action."}), 400

