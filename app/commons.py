APP_NAME = "smanzel"

def build_topic_name(username, hub_name, port):
    _TOPIC_TEMP = APP_NAME + "/{username}/{hub_name}/{port}"
    return _TOPIC_TEMP.format(username=username, hub_name=hub_name, port=port)