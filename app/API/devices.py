from flask import jsonify, request, Response, abort
from app import app
from app.models import Device, User, RevokedToken
from app.JSONSchemas import DeviceSchema, ValidationError
from flask_jwt_extended import jwt_required, get_jwt_identity


@app.route("/api/v1/devices", methods=["GET", "POST"])
@jwt_required
def devices():
    payload = get_jwt_identity()
    user_id = payload["id"]
    if request.method == "GET":
        devices = Device.by_owner(user_id)
        res = {
            "status": "success",
            "devices": DeviceSchema(many=True).dump(devices)
        }
        return jsonify(res)

    if request.method == "POST":
        """Create new device. Example:
            POST the JSON "{'port': 14, 'name': 'TV', 'place': 'room2', 'type': 1}"
            return device object if data is valid
            if the port already has a device update to the new parameters
        """

        json_data = request.get_json()
        device_schema = DeviceSchema()

        owner = User.get_by_id(user_id)
        try:
            device_schema.load(json_data)
            new_device = Device(
                name=json_data["name"],
                port=json_data["port"],
                place=json_data["place"],
                d_type=json_data["type"],
                owner=owner
            )
            new_device.save()
        except ValidationError as e:
            res = {
                "status": "validation failed",
                "messages": e.messages
            }
            return jsonify(res), 400

        res = {
            "status": "sucess",
            "device": device_schema.dump(new_device)
        }
        return jsonify(res), 201


@app.route("/api/v1/devices/<key>", methods=["GET", "PUT", "DELETE"])
@jwt_required
def device(key):
    target_device = Device.by_key(key)
    if target_device is None:
        return jsonify({
            "status": "not found",
            "message": "no device found by the key {}".format(key)
        }), 404

    if str(target_device.owner.id) != get_jwt_identity()['id']:
        return jsonify({
            "status": "failed",
            "message": "you do not have the required permisson"
        }), 403

    if request.method == "GET":
        return jsonify({
            "status": "success",
            "device": DeviceSchema().dump(target_device)
        })

    if request.method == "DELETE":
        target_device.delete()
        return jsonify({
            "status": "success",
            "message": "deleted successfully"
        }), 204


@app.route("/api/v1/device/action", methods=["PUT"])
@jwt_required
def deviceaction():
    # WARNING
    # NOT USED ANYMORE
    """ Turn on / Turn off device from the Dashboard
    Example : PUT -d '{hub_id: 123abc, port: 10, is_on: True}'
    :return 200
    """
    return jsonify("Soon"), 404
