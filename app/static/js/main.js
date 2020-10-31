var api_url = window.location.origin + "/api/v1";
var action_url = api_url + "/device/action";

function restMethod(method, url, data, onSuccess, onFailure) {
    console.log("restMethod", { url: url, data: data });
    return $.ajax({
        method: method,
        url: url,
        contentType: "application/json",
        dataType: "JSON",
        data: data,
        success: onSuccess,
        error: onFailure
    });
}

function toggle_device(hub_id, port, is_on, topic) {
    console.log("Is Topic Available ", topic)
    //    if topic is provided use mqtt
    var port = parseInt(port);
    var is_on = is_on == "true" ? true : false;
    if (topic) {
        let payload = is_on ? "0" : "1";
        client.publish(topic, payload);
    }
    var data = { "hub_id": hub_id, "port": port, "is_on": !is_on };
    var url = "/api/v1/device/action"
    restMethod("PUT", url, JSON.stringify(data))
        .done(function (device) {
            toggle_button(device);
        });
};

function toggle_button(device) {
    var device_dom = $('#' + device.id.$oid + ' .options .action');
    if (device.is_on == true) {
        device_dom.removeClass('btn-secondary')
            .data('is_on', 'true')
            .text('TURN OFF')
            .addClass('btn-primary');
    } else {
        device_dom.removeClass('btn-primary')
            .data('is_on', 'false')
            .text('TURN ON')
            .addClass('btn-secondary');
    }
}


function formToDevice(form) {
    var name = form.find('#name').val();
    var place = form.find('#place').val();
    var port = form.find('#port').val();
    var d_type = form.find('#type').val();
    return {
        name: name,
        place: place,
        port: parseInt(port),
        type: d_type
    }
}

function get_all_devices() {
    // get all devices from data base and call update_device to render new values
    var url = api_url + '/devices';
    restMethod("GET", url)
        .done(function (result) {
            console.log(result);
        })
};

$(document).ready(function () {

    var newDeviceForm = $('#newDeviceForm');
    newDeviceForm.on('submit', function (event) {
        console.log("onSubmit", "new device form");
        event.preventDefault();
        var url = api_url + "/devices"
        var data = formToDevice(newDeviceForm);
        console.log("new device form data", data);
        // submit via ajax
        restMethod("POST",
            url,
            JSON.stringify(data),
            (result => {
                console.log("New device is created");
                location.reload();
            }));
    });

    var btnDeleteDevice = $("[data-target=btnDeleteDevice]");
    btnDeleteDevice.on("click", function (event) {
        console.log("btnDeleteDevice")
        event.preventDefault();
        var key = $(event.target).data("key");
        var url = api_url + "/device/" + key
        console.log("Delete URL", url);
        restMethod("DELETE",
         url, 
         {}, // no data needed
        (res) => {
            console.log("Delete Device Res", res);
            // console.log(res);
            location.reload();
        },
        (err => {
            console.error("Delete Device Failed", err);
        })
        )
    
    });

    console.log('main loadded');

});