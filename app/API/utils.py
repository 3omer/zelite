from functools import wraps
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from flask import current_app as app
def turn_on(id):
    pass

def turn_off(id):
    pass

def get_state(id):
    pass


def token_required(view):
    """Inject apikey from header X-Api-Key into the global object 'g' as token
    @:param view: flask view function
    @:return: flask view
    """
    @wraps(view)
    def decorated_view(*args, **kwargs):
        key = request.headers.get("x-api-key")
        if key:
            g.token = key
            return view(*args, **kwargs)
        else:
            return jsonify(error="Unauthorized"), 401
    return decorated_view


def turn_off_switch(device):
    """Publish 0 to MQTT broker
        :@return: Ture if operation successed
    """
    mqtt_seetings = app.config["MQTT_SETTINGS"]
    hostname = mqtt_seetings["host"]
    port = mqtt_seetings["port"]
    try:
        publish.single(device.topic, payload="0", qos=1, retain=True,\
                hostname=hostname, port=1883, client_id="SERVER", \
                keepalive=5, will=None,auth = {'username':"omer",\
                'password':"ulvuelhk"}, tls=None, protocol=mqtt.MQTTv311, transport="tcp")
        return True
    except Exception as error:
        print("MQTT failed", error)
        return False