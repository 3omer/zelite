# Remote Services Calls

from threading import Thread
import jwt
from flask import url_for
from flask_mail import Message
from . import app
from . import mail


def send_async(app, msg):
    with app.app_context():
        mail.send(msg)


def send_verification_mail(recipient, token):
    link = url_for('verify_email', token=token, _external=True)
    print("USER EMAIL CONFIRMATION LINK: ", link)
    msg = Message('Zelite Account Verification', sender="omarosmandev@gmail.com",
                  recipients=[recipient])

    msg.body = 'Click the link below to activate your account ' + link
    msg.html = "<h2>Zelite Platform</h2><P>Welcome To Zelite IoT Platform Click activate to verify your account</p> \
    <a href={} >activate</a>".format(link)
    # mail.send(msg)
    Thread(target=send_async, args=(app, msg)).start()


def send_password_reset_mail():
    pass
