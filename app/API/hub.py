from flask import jsonify, request, abort, g
from app import app
from app.mongoDB import Hub, Device
from .utils import token_required

BASE_URL = "/api/v1/hub/{}"

# TODO response should have no cookie !


def port_and_status(s_devices):
    """map a device object to an object that has only port and status only"""
    return [{"port": device.port, "is_on": device.is_on} for device in s_devices]


@app.route("/api/v1/hub/devices", methods=["GET", "PUT"])
@token_required
def connected_devices():
    """call GET returns switched devices status, Notice hub only need the port and the status at the port
    Example: [
            {
                port: 12,
                is_on: false
            },
            {
                port: 14,
                is_on: true
            }
        ]

        Call PUT updates sensors data.
        Example: your hub must send (port, value) parameters for all devices
           [{
               port:2,
               value: 35.5
           },
           {
               port: 4,
               value: 20
           }
           ]
           """

    token = g.get("token")

    hub = Hub.by_token(token)
    if not (hub and hub.devices):
        return jsonify(error="No hub found or Incorrect Api Key"), 400

    devices = hub.devices
    switched_devices = devices.filter(type=Device.TYPES['switch'])
    sensord_devices = devices.filter(type=Device.TYPES['sensor'])

    if request.method == "GET":
        if switched_devices.count() > 0:
            return jsonify(port_and_status(switched_devices))

    if request.method == "PUT":
        data = request.get_json()
        if len(data) < 1:
            return abort(401, message="Invalid data.")

        for device in data:
            port = device.get('port')
            value = device.get('value')
            if (port is None) or (value is None):
                continue
            target_device = sensord_devices.filter(port=port).first()
            if target_device and target_device.value != value:
                target_device.value = float(value)

        hub.save()
        return jsonify(message="success")
