var api_url = "https://" + window.location.host + "/api/v1";
var action_url = api_url + "/device/action";

function restMethod(method, url, data, onSuccess) {
    return $.ajax({
        method: method,
        url: url,
        contentType: "application/json",
        dataType: "JSON",
        data: data,
        success: onSuccess
    });
}

function toggle_device(hub_id, port, is_on) {
    var port = parseInt(port);
    var is_on = is_on == "true" ? true: false;
    var data = {"hub_id":hub_id , "port":port , "is_on": !is_on};
    var url = "/api/v1/device/action"
    restMethod("PUT", url, JSON.stringify(data))
    .done(function(device) {
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


function getFormData(form) {
    var name = form.find('#name').val();
    var place = form.find('#place').val();
    var port = form.find('#port').val();
    var type = form.find('#type').val();
    return {
        name: name,
        place: place,
        port: parseInt(port),
        type: parseInt(type)
    }
}

function get_all_devices() {
    // get all devices from data base and call update_device to render new values
    var url = api_url + '/devices';
    restMethod("GET", url)
    .done(function(result) {
        console.log(result);
        })
};

function update_device(device){
    var selector ='#' + device.id.$oid;
    var device_card = $(selector);
    device_card.find('[data-target=name]').text(device.name);
    device_card.find('[data-target=place]').text(device.place);
    // device_card.find('[data-target=is_on]');
    if (device.type == 2) {
       device_card.find('[data-value]').text(device.value);
    } else {
        toggle_button()
    }
}

$(document).ready(function () {
    // prevent click on turn on / turn off btns
    $('.action').click(function (event) {
        event.preventDefault();
        var hub_id = $(this).data('hub');
        var port = $(this).data('port');
        var is_on = $(this).data('is_on').toString();
        console.log('port: ' + port + ' is_on ' + is_on);
        toggle_device(hub_id, port, is_on);
    });

    var newDeviceForm = $('.device_form');
    newDeviceForm.on('submit', function (event) {
        event.preventDefault();
        var url = api_url + "/devices"
        var data = getFormData($(this));
        var hub_id = $(this).data("hub_id");
        data.hub_id = hub_id;
        console.log(data);
        // submit via ajax
        restMethod("POST", url, JSON.stringify(data))
        .done(function(result) {
            console.log("Posted");
            location.reload();
        });

    });

    $("#hub_form").on("submit", function(event) {
        event.preventDefault();
        var url = api_url + "/hubs";
        var data = getFormData($(this));
        restMethod("POST", url, JSON.stringify(data), function(result) {
            console.log("POST new hub");
            console.log(result);
            location.reload();
        });
    });

    var delete_device_btn = $(".delete_device");
    delete_device_btn.on("click", function(event) {
        event.preventDefault();
        var url = api_url + "/device"
        var hub_id = $(this).data("hub_id");
        var port = $(this).data("port");
        var data = JSON.stringify({ "hub_id": hub_id, "port": port });
        restMethod("DELETE", url, data)
        .done(function(result) {
            console.log("Delete operation");
            console.log(result);
            location.reload();
        });
    });

    var delete_hub_btn = $(".delete_hub");
    delete_hub_btn.on("click", function(event) {
        event.preventDefault();
        var url = api_url + "/hubs";
        var hub_id = $(this).data("hub_id");
        restMethod("DELETE", url, JSON.stringify({"hub_id": hub_id}))
        .done(function(result) {
            console.log("Delte hub request done");
            console.log(result);
            location.reload();
        });

    });

    // setInterval(() => {
    //    devices = get_all_devices();
//    update_devices(devices)
    // }, 5000);

    console.log('main loadded');

});