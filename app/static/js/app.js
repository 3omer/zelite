function renderSwitch($ele, data) {
    if (data === '1') {
        $ele.removeClass('btn-secondary')
            .data('state', '1')
            .text('TURN OFF')
            .addClass('btn-primary');
    } else if (data === '0') {
        $ele.removeClass('btn-primary')
            .data('state', '0')
            .text('TURN ON')
            .addClass('btn-secondary');
    }
};
function renderSesnor($ele, data) {
    $ele.text(data);
};

function toggleSwitch(topic, currentState) {
    console.log(`Toggling Switch State: from ${currentState}`);
    if (currentState === "0") {
        console.log("To: ", "1");
        client.publish(topic, "1", 1, true);
    } else if (currentState === "1") {
        console.log("To: ", "0");
        client.publish(topic, "0", 1, true);
    }
}

function handleMessage(message) {
    let $ele = $(`[data-topic_name='${message.topic}']`);
    if (!$ele.length) return;  // no element by that topics its old subscribtion, discard
    let isSwitch = $ele.data('target') == "switch";
    if (isSwitch) renderSwitch($ele, message.payloadString);
    else renderSesnor($ele, message.payloadString);
}

// MQTT Client-API
function mqttManager(){
    let mqttHost = '127.0.0.1';
    let port = 8000;
    let clientID = 'smanzel-123';
    let client = new Paho.MQTT.Client(mqttHost, port, clientID);

    // set callback handlers
    client.onConnectionLost = (responseObject) => {
        if (responseObject.errorCode !== 0) {
            console.log("onConnectionLost:" + responseObject.errorMessage);
        }
    };


    client.onMessageArrived = (message) => {
        console.log("onMessageArrived:", message.topic, message.payloadString);
        handleMessage(message);
    }

    let onConnect = () => {
        console.log('---- connected ----');
        console.log("Subscribing to User's Topics: ");
        // smanzel/username/hub_name/port
        client.subscribe('smanzel/omer/+/+', { qos: 1, onFailure: console.log, onSuccess: console.log });
    }

     client.publish = (topic, payload) => {
        console.log('----publishing --');
        console.log('Topic: ', topic, 'Message: ', payload)
        let message = new Paho.MQTT.Message(payload);
        message.destinationName = topic;
        client.send(message);
        console.log('Published: ', message);
    }

    let onFailure = (err) => console.log(err);
    // open connection
    client.connect({ onSuccess: onConnect, onFailure: onFailure });
};


$(document).ready(function () {
    // clicking action buttons publish events
    $('.action').click(function (event) {
    event.preventDefault();
        let $ele = $(this);
        let topic = $ele.data('topic_name');
        let state = $ele.data('state');
        console.log('Switch Action:');
        console.log('topic: ', topic, ' state: ', state);
        toggleSwitch(topic, state);
    });

});

 /*
    *
    * MQTT CLIENT CODE
    *
    */
    let mqttHost = MQTT_SETTINGS.host;
    let port = MQTT_SETTINGS.port;
    let clientID = 'smanzel-123';
    let client = new Paho.MQTT.Client(mqttHost, port, clientID);

    // set callback handlers
    client.onConnectionLost = (responseObject) => {
        if (responseObject.errorCode !== 0) {
            console.log("onConnectionLost:" + responseObject.errorMessage);
        }
    };


    client.onMessageArrived = (message) => {
        console.log("onMessageArrived:", message.topic, message.payloadString);
        handleMessage(message);
    }

    let onConnect = () => {
        console.log('---- connected ----');
        console.log("Subscribing to User's Topics: ");
        // smanzel/username/hub_name/port
        MQTT_TOPIC_LIST.forEach(topic => {
            client.subscribe('smanzel/omer/+/+', { qos: 1, onFailure: console.log, onSuccess: console.log });
        })
    }

//    let publish = (topic, payload) => {
//        console.log('----publishing --');
//        console.log('Topic: ', topic, 'Message: ', payload)
//        let message = new Paho.MQTT.Message(payload);
//        message.destinationName = topic;
//        client.send(message, 1, true);
//        console.log('Published: ', message);
//    }

    let onFailure = (err) => console.log(err);
    // open connection
    client.connect({useSSL: MQTT_SETTINGS.useSSL === "true" ,onSuccess: onConnect, onFailure: onFailure, reconnect: true });
