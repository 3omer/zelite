# Remote Services Calls

import jwt
from flask import url_for
from flask_mail import Message
from . import app
from . import mail


def send_verification_mail(recipient, token):
    msg = Message('Zelite Account Verification', sender="admin@zelite.com",
                  recipients=[recipient])

    link = url_for('verify_email', token=token, _external=True)
    msg.body = 'Click the link below to activate your account ' + link
    msg.html = "<h2>Zelite Platform</h2><P>Welcome To Zelite IoT Platform Click activate to verify your account</p> \
    <a href={} >activate</a>".format(link)
    mail.send(msg)


def send_password_reset_mail():
    pass
