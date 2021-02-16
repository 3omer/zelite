# Zelite

**Zelite** is an IoT platform to monitor and manage home devices "Lights, Fans, TV ..etc". Basically you can control any device by connecting it to a relay that has an internet connection.
It's composed of a REST API for AuthN/AuthZ and devices management.
The actual messaging between end devices "IoT" and the front end is done through MQTT broker.


> Live Demo: [on heroku](https://zelite.herokuapp.com)

*Note: The live demo is using the public MQTT Broker [test.mosquitto.org](test.mosquitto.org). It's unreliable and messages aren't persistent*

## The Architecture
![Project Architecure](https://github.com/3omer/zelite/blob/master/spec/arch.jpg?raw=true)

This Repo is implementing the Web-Server App part from the architecture.


## RESET-API
Check the Postman collection [here](https://github.com/3omer/zelite/blob/master/spec/Zelite%20Platform.postman_collection.json)
