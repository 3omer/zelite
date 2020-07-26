from flask import request, redirect, url_for, render_template, flash
from app import app, login_manager
from flask_login import login_required, current_user, login_user, logout_user
from app.mongoDB import User, NotUniqueError
import logging
log = logging.getLogger()

@login_manager.user_loader
def load_user(id):
    return User.get_by_id(id)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        try:
            User.register(request.form)
            flash("Registered Successfully", "success")
            return redirect(url_for("login"))
        except NotUniqueError as e:
            log.error(e)
            flash("This Username/Email Already Exist, Try another one", "error")

    return render_template("register.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.get_by_email(email)
        if user is not None and user.check_password(password):
            flag = login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Email or Password is inncorect.')
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    if not current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    logout_user()
    return redirect(url_for('login'))
