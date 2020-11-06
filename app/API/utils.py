from functools import wraps
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import paho.mqtt.subscribe as subscribe
from flask import current_app as app


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


def set_switch_state(device, state):
    """Publish 0 to MQTT broker
        :@state: '0' or '1'
        :@return: Ture if operation successed
    """
    mqtt_seetings = app.config["MQTT_SETTINGS"]
    hostname = mqtt_seetings["host"]
    port = mqtt_seetings["port"]
    try:
        publish.single(device.topic, payload=state, qos=1, retain=True,\
                hostname=hostname, port=1883, client_id="SERVER", \
                keepalive=5, will=None,auth = {'username':"omer",\
                'password':"omer"}, tls=None, protocol=mqtt.MQTTv311, transport="tcp")
        return True
    except Exception as error:
        print("MQTT failed", error)
        return False


def read_sensor(device):
    
    mqtt_seetings = app.config["MQTT_SETTINGS"]
    hostname = mqtt_seetings["host"]
    port = mqtt_seetings["port"]
    
    try:
        val = publish.single(device.topic, qos=1,\
                hostname=hostname, port=1883, client_id="SERVER", \
                keepalive=5, will=None,auth = {'username':"omer",\
                'password':"omer"}, tls=None, protocol=mqtt.MQTTv311, transport="tcp")
        return val
    except Exception as error:
        print("MQTT failed", error)
        return None
