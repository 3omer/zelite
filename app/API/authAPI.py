import re
from flask import request, jsonify
from flask_jwt_extended import jwt_required, create_access_token, get_raw_jwt
from app import app, jwt_manager
from app.models import RevokedToken, User, NotUniqueError, ValidationError


# initialize jwt loader
@jwt_manager.token_in_blacklist_loader
def token_black_listed_loader(dec_token):
    jti = dec_token["jti"]
    return RevokedToken.is_blacklisted(jti)


@app.route("/api/v1/register", methods=["POST"])
def register():
    if request.method == "POST":
        try:
            User.register(request.get_json())
            return jsonify({ "message": "Registered Successfully" }), 201
        except NotUniqueError as e:
            # log.error(e)
            filed = "Username" if re.search("username", str(e)) else "Email"
            return jsonify({ "error": "This {} Already Exist, Try another one".format(filed)}), 400
        except ValidationError as e:
            return jsonify({ "error": "Invalid data. Please make sure you submited complete form"}), 400

@app.route("/api/v1/login", methods=["POST"])
def jwt_login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
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
    res["username"] = user.username
    res["email"] = user.email
    
    return jsonify(res)


@app.route("/api/v1/logout", methods=["POST"])
@jwt_required
def revoke_token():
    jti = get_raw_jwt()["jti"]
    RevokedToken.add(jti)
    return jsonify({"message": "Successuflly logged out"}), 200