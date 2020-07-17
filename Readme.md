# Manzel 
**Manzel** is an IoT platform to monitor and manage home devices "Lights, Fans, TV ..etc". Basically you can control any device by connecting it to a relay that has an internet connection.
	
## Main Components
 - **User Dashboard**
 - **Home-Hub**
	
## Data Flow 
**End User** start adding devices after creating account and get API keys. Then from a dashboard End user can **turn on/ turn off** their devices and get sensors updates if any.    
**Relays** communicate with the server by continuously hitting a RESET API to sync their states.

## RESET-API
