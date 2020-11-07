from flask import jsonify, request, abort
from app import app
from app.mongoDB import Device, User
from .utils import set_switch_state, read_sensor
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
    user_id = data.get("user_id")
    try:
        name = data.get("name")
        place = data.get("place")
        action = data.get("action")
    except Exception as e:
        return jsonify({"error": "Provide a name, a place and an action."}), 400

    user = User.objects().first() # this is just for testing
    user = User.get_by_id(user_id)
    print("user", user.id, "req_param", user_id)
    
    # get the device then filter them by name
    devices = Device.by_owner(user)
    target_device = None
    target_device = devices.filter(name=name, place=place).first()

    if not target_device:
        return jsonify({"error": "Not found"}), 404

    if action == "read":
        val = read_sensor(target_device)
        if val :
            return jsonify({"data": val})
        return jsonify(), 500


    flag = False
    if action == "turn_on":
        flag = set_switch_state(target_device, "1")
    elif action == "turn_off":
        flag = set_switch_state(target_device, "0")

    else:
        return jsonify({"error": "Unknown Action."}), 400
    
    if flag:
        return jsonify({"data": "success"}), 200
    return jsonify("Internal Error"), 500
        
