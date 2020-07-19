from flask import jsonify, request, Response, abort
from app import app
from flask_login import login_required, current_user
from app.mongoDB import Hub, Device, User
from app.API.utils import doesnt_exist

""" These API are meant to be access from the web client 'Dashboard' """

# : These API are authenticated with a session, Should authenticate with key


@app.route("/api/v1/hubs", methods=["POST", "DELETE"])
@login_required
def hubs():
    if request.method == "POST":
        name = request.get_json()["name"]
        hub = Hub(name=name)
        owner = User.get_by_id(current_user.id)
        hub.owner = owner
        hub.save()
        return jsonify(), 201

    if request.method == "DELETE":
        hub_id = request.get_json()["hub_id"]
        target_hub = Hub.by_id(hub_id)
        target_hub.delete()
        target_hub.save()

        return jsonify(), 204



@app.route("/api/v1/devices", methods=["GET", "POST"])
@login_required
def devices():

    if request.method == "GET":
        hubs = Hub.by_owner(current_user)
        return hubs.to_json()

    if request.method == "POST":
        """Create new device. Example:
            POST the JSON "{'port': 14, 'name': 'TV', 'place': 'room2', 'type': 1}"
            return device object if data is valid
            if the port already has a device update to the new parameters
        """
        args = request.get_json()
        hub_id = args.get("hub_id")
        port = args.get('port')
        name = args.get('name')
        place = args.get('place')
        type = args.get('type')
        # check if data is valid
        hub = Hub.by_id(hub_id)
        device = hub.get_device(port)
        if device is not None:
            device.name = name
            device.place = place
            device.type = type

        else:
            device = Device(
                port=port,
                name=name,
                place=place,
                type=type
            )
            hub.devices.append(device)

        hub.save()
        return jsonify(), 201


@app.route("/api/v1/device", methods=["GET", "PUT", "DELETE"])
@login_required
def device():
    """ Access specific device by its hub id and hub port"""

    args = request.get_json()
    hub_id = args["hub_id"]
    port = args["port"]
    hub = Hub.by_id(hub_id)
    target_device = hub.get_device(port)

    if target_device is None:
        return doesnt_exist(port)

    if request.method == "GET":
        return jsonify(target_device)

    if request.method == "PUT":
        target_device.name = args['name']
        target_device.port = args['port']
        target_device.type = args['type']
        target_device.place = args['place']
        target_device.value = args.get('value', None)
        target_device.is_on = args.get('is_on', False)
        hub.save()
        return jsonify(target_device)
    
    if request.method == "DELETE":
        hub.update(pull__devices__id=target_device.id)
        hub.save()
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
    hub = Hub.by_id(hub_id)
    target_device = hub.get_device(port)

    if target_device is None:
        return doesnt_exist(port=port)
    target_device.is_on = is_on
    hub.save()
    # convert object id to string
    # target_device.id = str(target_device.id)
    return target_device.to_json()
