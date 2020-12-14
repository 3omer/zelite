from flask import jsonify, request, Response, abort
from app import app
from flask_login import login_required, current_user
from app.mongoDB import Device, User, RevokedToken, ValidationError
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_raw_jwt

""" These API are meant to be accessed from the web client 'Dashboard' """
# : These API are authenticated with a session, Should authenticate with key


@app.route("/api/v1/login", methods=["POST"])
def jwt_login():
    data = request.get_json()
    email = data.get("email", None)
    password = data.get("password", None)
    print(email, password)
    res = {}
    if not email:
        res["error"] = "Missing email parameter"
        return jsonify(res), 400
    if not password:
        res["error"] = "Missing password parameter"
        return jsonify(res), 400
    
    user = User.get_by_email(email)
    if not ( user and user.check_password(password)):
        res["error"] = "Invalid credentials"
        return jsonify(res), 401
    
    token = user.generate_token()
    res["token"] = token
    return jsonify(res)


@app.route("/api/v1/logout", methods=["POST"])
@jwt_required
def token_revoke():
    dec_token = get_raw_jwt()
    RevokedToken.add(dec_token)
    return jsonify(dec_token), 200
    

@app.route("/api/v1/devices", methods=["GET", "POST"])
@jwt_required
def devices():
    """GET -> user's devices -
    POST -> Create new device"""
    payload = get_jwt_identity()
    user_id = payload["id"]
    if request.method == "GET":
        devices = Device.by_owner(user_id)
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
@jwt_required
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
@jwt_required
def deviceaction():
    """ Turn on / Turn off device from the Dashboard
    Example : PUT -d '{hub_id: 123abc, port: 10, is_on: True}'
    :return 200
    TODO return updated code with no body
    """
    return jsonify("Soon"), 404
