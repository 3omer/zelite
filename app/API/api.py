from flask import jsonify, request, Response, abort
from app import app
from flask_login import login_required, current_user
from app.mongoDB import Device, User, ValidationError
from flask_jwt_extended import create_access_token

""" These API are meant to be accessed from the web client 'Dashboard' """
# : These API are authenticated with a session, Should authenticate with key


@app.route("/api/login", methods=["POST"])
def jwt_login():
    username, password = request.get_json() or (None, None)
    res = {}
    if not username:
        res.error = "Missing username parameter"
        return jsonify(res), 400
    if not password:
        res.error = "Missing password parameter"
        return jsonify(res), 400
    
    if not User.check_password(username, password):
        res.error = "Invalid credentials"
        return jsonify(res), 401
    
    user = User.get_by_username(username)
    if not user:
        res.error = "User not found"
        return jsonify(res), 404
    
    token = create_access_token(identity=username)
    return jsonify(token)
    






@app.route("/api/v1/devices", methods=["GET", "POST"])
@login_required
def devices():
    """GET -> user's devices -
    POST -> Create new device"""

    if request.method == "GET":
        devices = Device.by_owner(current_user.id)
        return jsonify(devices)

    if request.method == "POST":
        """Create new device. Example:
            POST the JSON "{'port': 14, 'name': 'TV', 'place': 'room2', 'type': 1}"
            return device object if data is valid
            if the port already has a device update to the new parameters
        """
        args = request.get_json()
        port = args.get('port')
        name = args.get('name')
        place = args.get('place')
        d_type = args.get('type')

        new_device = Device(name=name, port=port, place=place, d_type=d_type, owner=current_user.id)
        try:
            new_device.save()
        except ValidationError as e:
            return jsonify(), 400
        except Exception as e:
            return jsonify(), 500
        return jsonify(), 201


@app.route("/api/v1/device/<key>", methods=["GET", "PUT", "DELETE"])
@login_required
def device(key):
    """ Access specific device by its key"""

    target_device = Device.by_key(key)
    if target_device is None:
        return jsonify(), 404

    if request.method == "GET":
        return jsonify(target_device)

    if request.method == "DELETE":
        target_device.delete()
        return jsonify("deleted"), 204
        

@app.route("/api/v1/device/action", methods=["PUT"])
@login_required
def deviceaction():
    """ Turn on / Turn off device from the Dashboard
    Example : PUT -d '{hub_id: 123abc, port: 10, is_on: True}'
    :return 200
    TODO return updated code with no body
    """

    args = request.get_json()
    hub_id = args["hub_id"]
    port = args['port']
    is_on = args['is_on']
    hub = {} # Hub.by_id(hub_id)
    target_device = {} # hub.get_device(port)

    if target_device is None:
        return doesnt_exist(port=port)
    target_device.is_on = is_on
    hub.save()
    # convert object id to string
    # target_device.id = str(target_device.id)
    return target_device.to_json()
