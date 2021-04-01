import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import paho.mqtt.subscribe as subscribe
from flask import current_app as app


MQTT_USERNAME = "admin"
MQTT_PWD = "admin"
MQTT_ID = "SERVERADMIN"

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
                hostname=hostname, port=1883, client_id=MQTT_ID, \
                keepalive=5, will=None,auth = {'username':MQTT_USERNAME,\
                'password':MQTT_PWD}, tls=None, protocol=mqtt.MQTTv311, transport="tcp")
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
                hostname=hostname, port=1883, client_id=MQTT_ID, \
                keepalive=5, will=None,auth = {'username':MQTT_USERNAME,\
                'password':MQTT_PWD}, tls=None, protocol=mqtt.MQTTv311, transport="tcp")
        return val
    except Exception as error:
        print("MQTT failed", error)
        return None

def validate_user_mqtt(user, username, password):
    if user.mqtt_username == username and user.mqtt_password == password:
        return True
    return False

def is_mqtt_admin(username, password):
    if username == MQTT_USERNAME and password == MQTT_PWD:
        return True
    return False