from app import app
from flask import render_template, request, url_for, redirect, flash
from app.mongoDB import Device, Hub
from app.mongoDB import User
from flask_login import login_required, current_user
from app.utils import map_hubs


@app.route('/')
@app.route('/dashboard')
@login_required
def dashboard():
    hubs = Hub.by_owner(current_user.id) #this should not work but it works. by_owner take User object not id!
    hubs_mapped = map_hubs(hubs)
    return render_template('index.html', hubs=hubs_mapped)


@app.route('/manager')
@login_required
def manager():
    hubs = Hub.by_owner(current_user.id)
    return render_template('manager.html', hubs=hubs)