from flask import jsonify, request, abort, Response, redirect, url_for
from flask_login import current_user, login_required
from app import app
from app.mongoDB import Device, User
from app.API.utils import validate_user_mqtt, is_mqtt_admin

# api for mqtt authentication
@login_required
@app.route("/api/v1/mqtt/create", methods=["POST"])
def mqtt_credentials():
    """create MQTT credentials """
    username = request.form.get('username')
    password = request.form.get('password')
    
    if current_user:
        current_user.mqtt_username = username
        current_user.mqtt_password = password
        current_user.save()
    return redirect(url_for("manager"))

@app.route("/api/v1/mqtt/auth", methods=["POST"])
def authMqtt():
    username = request.form.get('username')
    password = request.form.get('password')
    topic    = request.form.get('topic')
    acc      = request.form.get('acc')

    user = User.get_by_mqtt_username(username)
    if is_mqtt_admin(username, password):
        return Response("", 200)
    if user and validate_user_mqtt(user, username, password):
        return Response("", 200)
    return abort(400)

@app.route("/api/v1/mqtt/superuser", methods=["POST"])
def superuser():
    username = request.form.get('username')
    password = request.form.get('password')

    if username == "admin" and password == "admin": # these are just default .. change them
        return Response("", 200)
    return abort(400)

@app.route("/api/v1/mqtt/acl", methods=["POST"])
def acl():

    username = request.form.get('username')
    topic    = request.form.get('topic')
    clientid = request.form.get('clientid')
    acc      = request.form.get('acc') # 1 == SUB, 2 == PUB

    if username == "admin":
        return Response("", 200)

    user = User.get_by_mqtt_username(username)
    if user and (topic in user.topics):
        return Response("", 200)
    return abort(400)
    
            