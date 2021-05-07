from flask import jsonify, request, abort, Response, redirect, url_for
from app import app
from app.models import Device, User
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.API.utils import validate_user_mqtt, is_mqtt_admin
from app.JSONSchemas import MqttCredSchema, ValidationError


@app.route("/api/v1/mqtt", methods=["GET", "POST"])
@jwt_required
def mqtt_credentials():

    user_id = get_jwt_identity()["id"]
    current_user = User.get_by_id(user_id)

    if request.method == "GET":
        return jsonify({
            "status": "sucess",
            "credentials": {
                "username": current_user.mqtt_username,
                "password": current_user.mqtt_password,
            },
            "topics": current_user.topics
        })

    if request.method == "POST":
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        errors = MqttCredSchema().validate(data)

        if not errors:
            current_user.mqtt_username = username
            current_user.mqtt_password = password
            current_user.save()
            return jsonify({
                "status": "success",
                "credentials": {
                    "username": current_user.mqtt_username,
                    "password": current_user.mqtt_password
                }
            })
        else:
            return jsonify({
                "status": "validation failed",
                "error":  errors
            }), 400


@app.route("/api/v1/mqtt/auth", methods=["POST"])
def authMqtt():
    username = request.form.get('username')
    password = request.form.get('password')
    # topic = request.form.get('topic')
    # acc = request.form.get('acc')

    if is_mqtt_admin(username, password):
        return Response("", 200)

    user = User.get_by_mqtt_username(username)
    if not user:
        return abort(401)

    if user.validate_mqtt(username, password):
        return Response("", 200)
    return abort(401)


@app.route("/api/v1/mqtt/superuser", methods=["POST"])
def superuser():
    username = request.form.get('username')
    password = request.form.get('password')

    if username == "admin" and password == "admin":  # this is bad
        return Response("", 200)
    return abort(400)


@app.route("/api/v1/mqtt/acl", methods=["POST"])
def acl():

    username = request.form.get('username')
    topic = request.form.get('topic')
    clientid = request.form.get('clientid')
    acc = request.form.get('acc')  # 1 == SUB, 2 == PUB

    if is_mqtt_admin(username, "admin"):
        return Response("", 200)

    user = User.get_by_mqtt_username(username)
    if user and user.has_topic(topic):
        return Response("", 200)
    return abort(403)
