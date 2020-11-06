from flask import jsonify, request, abort, Response
from app import app
from app.mongoDB import Device, User

# api for mqtt authentication
@app.route("/api/v1/mqtt/auth", methods=["POST"])
def authMqtt():
    username = request.form.get('username')
    password = request.form.get('password')
    topic    = request.form.get('topic')
    acc      = request.form.get('acc')

    if username == password:
        return Response("", 200)
    return abort(400)

@app.route("/api/v1/mqtt/superuser", methods=["POST"])
def superuser():
    username = request.form.get('username')
    password = request.form.get('password')

    if username == "admin":
        return Response("", 200)
    return abort(400)

@app.route("/api/v1/mqtt/acl", methods=["POST"])
def acl():

    username = request.form.get('username')
    topic    = request.form.get('topic')
    clientid = request.form.get('clientid')
    acc      = request.form.get('acc') # 1 == SUB, 2 == PUB

    return Response("", 200)