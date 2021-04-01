from app import app
from flask import render_template, request, url_for, redirect, flash
from app.models import Device, User
from flask_login import login_required, current_user


@app.route('/')
@app.route('/dashboard')
@login_required
def dashboard():
    devices = Device.by_owner(current_user.id)
    switch_devices = []
    sensor_devices = []
    for device in devices:
        if device.d_type == "switch":
            switch_devices.append(device)
        else:
            sensor_devices.append(device)

    return render_template('index.html', **{"switch_devices": switch_devices, "sensor_devices": sensor_devices})


@app.route('/manager')
@login_required
def manager():
    devices = Device.by_owner(current_user.id)
    return render_template('manager.html', devices=devices)


@app.route('/bot')
@login_required
def bot():
    return render_template('bot.html')

