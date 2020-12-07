# Manzel

**Manzel** is an IoT platform to monitor and manage home devices "Lights, Fans, TV ..etc". Basically you can control any device by connecting it to a relay that has an internet connection.
It's composed of a REST API for users managent and devices creation.
The actual messaging between end devices "IoT" and the front end is an MQTT connection.

## Live Demo:

 [on heroku](https://smanzel.herokuapp.com/)
> heroku free container does not support mqtt


## RESET-API

### Main-API:
**End-points:**

****These endpoints require authentication via cookie.****

    /api/v1/devices
	 
**Methods:**
POST: Create new device

        {'port': 14, 'name': 'TV', 'place': 'room2', 'type': 1}"


GET: Users devices list	

    [{ name: "fan", place: "room1", type: "sensor", port: 123, topic: "mqtt/topic" }, ... ]
 
 ---

    /api/v1/device/<id>

**Methods:**
GET: get a device .


DELETE: Delete a device.	

  ---

    /api/v1/device

**Methods:**
GET: specific device attached to a hub by providing: hub id and hub port.

        { hub_id: 123, port: 1}

PUT: Update device on hub providing its id.	

    { hub_id: 123, port: 1, name: 'light', place: 'room1', type: '1' }
    
DELETE:

    { hub_id: 123, port: 1}

  ---

    /api/v1/device/action

**Methods:**

PUT: Turn on / Turn off device.	

    {hub_id: 123abc, port: 10, is_on: True}
    
---
### HUB-API:
**These endpints are authenticated by API-KEY header `x-api-key`. 
Each hub is assigned a key on the dashboard** 


    /api/v1/hub/devices

**Methods:**

GET returns switched devices status, Notice hub only need the port and the status at the port  
 

    [{ port: 12, is_on: false }, 
     { port: 14, is_on: true }]


Call PUT updates to sensors data.  Your hub must send (port, value) parameters for all devices  
 

    [{ port:2, value: 35.5 }, 
    { port: 4, value: 20 } ]
