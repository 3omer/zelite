import re
from flask import request, jsonify
from flask_jwt_extended import jwt_required, create_access_token, get_raw_jwt
from app import app, jwt_manager
from app.models import RevokedToken, User, NotUniqueError, ValidationError
from app.JSONSchemas import UserSchema, ValidationError
from app.mailService import send_verification_mail

# initialize jwt loader


@jwt_manager.token_in_blacklist_loader
def token_black_listed_loader(dec_token):
    jti = dec_token["jti"]
    return RevokedToken.is_blacklisted(jti)


@app.route("/api/v1/register", methods=["POST"])
def register():
    user_schema = UserSchema()
    if request.method == "POST":
        json_data = request.get_json()
        try:
            user_schema.load(json_data)
            new_user = User.register(json_data)
            if app.config["SEND_EMAIL"]:
                send_verification_mail(
                    new_user.email, new_user.get_verification_token())
            else:
                new_user.verified = True
                new_user.save()
            return jsonify({
                "status": "success",
                "message": "Check your email to activate your aacount",
                "user": user_schema.dump(new_user)
            }), 201

        except ValidationError as e:
            return jsonify({
                "status": "failed",
                "messages": e.messages
            }), 400

        except NotUniqueError as e:
            # TODO: this is a tricky way to identify the path that raised the duplicate error
            # by searching in the error message
            mongo_error_message = str(e)
            filed = "username" \
                if re.search("username", mongo_error_message) \
                else "email"
            # for consistency structure the error as the marshamello-validaton-errors
            e = {
                "status": "validatoin failed",
                "messages": {
                    filed: [
                        "this {} is already registered".format(filed)]
                }
            }
            return jsonify(e), 400


@app.route("/api/v1/verify", methods=["GET"])
def verify_email():
    token = request.args.get("token")
    try:
        User.verify_account(token)
        return jsonify({
            "status": "success",
            "message": "Account has been activated"
        })
    except Exception as e:
        print(e)
        return jsonify({
            "status": "account activation failed",
            "message": "Invalid or expired link"
        }), 403


@app.route("/api/v1/login", methods=["POST"])
def jwt_login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    error_messages = {}
    if not email:
        error_messages["email"] = ["required field"]
    if not password:
        error_messages["password"] = ["required field"]

    if error_messages:
        return jsonify({
            "status": "validation failed",
            "messages": error_messages
        }), 400

    user = User.get_by_email(email)
    if not (user and user.check_password(password)):
        res = {
            "status": "login failed",
            "message": "email or password is woring"
        }
        return jsonify(res), 401

    if not user.verified:
        return jsonify({
            "status": "login failed",
            "message": "Confirm your account. Follow instruction sent to your email"
        }), 400

    token = user.generate_token()
    res = {
        "status": "success",
        "token": token,
        "user": UserSchema().dump(user)
    }
    return jsonify(res)


@app.route("/api/v1/logout", methods=["POST"])
@jwt_required
def revoke_token():
    jti = get_raw_jwt()["jti"]
    RevokedToken.add(jti)
    return jsonify({
        "status": "success",
        "message": "successuflly logged out"
    }), 200
