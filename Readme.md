# Manzel

**Manzel** is an IoT platform to monitor and manage home devices "Lights, Fans, TV ..etc". Basically you can control any device by connecting it to a relay that has an internet connection.

## Main Components

 - **User Dashboard**: A web portal where users can:
	 - Manage registerd Home-hub.
	 -  turn on/ off devices and get sensors updates if any.
 - **Home-Hub**: This is could be any IoT Board "ESP8266, Arduino .. etc" act as a RESET Client performing:
	 -  **GET** requests to fetch last Devices states.
	 - **PUT** to upload sensors data.
## Database Models

## RESET-API
The endpoints are logically separated into two module: 
**Main-API :** Manage user interaction with the resources.
**Hub-API:** Enables home hubs to sync their states. 

### Main-API:
**End-points:**

****These endpoints require authentication session cookie.****

    /api/v1/hubs
	 
**Methods:**
POST: Create new hub.

    { name: "my hub" }

DELETE:	

    { hub_id: 123 }
 
 ---

    /api/v1/devices

**Methods:**
GET: return current user devices .


POST: Add new device to a hub providing its id.	

    { hub_id: 123, port: 1, name: 'light', place: 'room1', type: '1' }
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
