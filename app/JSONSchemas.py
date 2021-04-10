from marshmallow import (Schema, fields, validate, ValidationError)


class UserSchema(Schema):
    id = fields.Str(dump_only=True)
    email = fields.Str(
        required=True, validate=[validate.Email(error="Not a valid email address")]
    )
    username = fields.Str(required=True,
                          validate=[
                              validate.Length(
                                  min=4, max=50, error="username must have between {min} and {max} characters."),
                              validate.Regexp(
                                  r"[a-zA-Z0-9_\-]*$", error="username must not contain special characters (except _ und -)"),
                              validate.ContainsNoneOf(
                                  [" "], error="username must not contain spaces")
                          ]
                          )
    password = fields.Str(
        required=True,
        load_only=True,
        validate=[
            validate.Length(
                min=8,
                max=30,
                error="password must have a length between {min} and {max}"
            )
        ]
    )

    mqtt_topics = fields.List(fields.Str, dump_only=True)


class DeviceSchema(Schema):
    key = fields.Str()
    name = fields.Str(required=True, validate=validate.Length(min=2))
    place = fields.Str(required=True, validate=validate.Length(min=2))
    port = fields.Int(validate=[validate.Range(min=0)])
    d_type = fields.Str(data_key="type", required=True, validate=[
                        validate.OneOf(["switch", "sensor"])])
    topic = fields.Str(
        validate=[
            validate.ContainsNoneOf(
                ["+", "#", " ", "*"], error="Invalid MQTT topic structure. Follow the standards defined by MQTT specifications."),
            lambda val: val.count("/") > 1
        ]
    )

class MqttCredSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)