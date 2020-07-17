from app.mongoDB import Device


def map_hubs(hubs):
    """map hubs to a list of dicts
    {'id':  'hub_id'
    'switch_devices': [],
    'sensor_device': []
    }

    :param hubs: Hub objects list
    :returns: [{str, list, list}]
    """
    hubs_mapped = []
    for hub in hubs:
        hub_mapped = {"id": hub.id, "switch_devices": [], "sensor_devices": []}
        for device in hub.devices:
            if device.type == Device.TYPES["switch"]:
                hub_mapped["switch_devices"].append(device)
            else:
                hub_mapped["sensor_devices"].append(device)
        hubs_mapped.append(hub_mapped)
    return hubs_mapped
