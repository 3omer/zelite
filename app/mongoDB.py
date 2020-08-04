from app import db
from bson.objectid import ObjectId
from mongoengine.errors import NotUniqueError, ValidationError
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import secrets


class User(UserMixin, db.Document):
    email = db.EmailField(max_length=50, unique=True)
    username = db.StringField(max_length=50, unique=True)
    password_hash = db.StringField(max_length=128)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @classmethod
    def register(cls, form):
        username = form.get("username")
        email = form.get("email")
        password = form.get("password")
        new_user = cls(username=username, email=email)
        new_user.set_password(password)
        new_user.save()


    @classmethod
    def get_by_email(cls, email):
        return cls.objects(email=email).first()

    @classmethod
    def get_by_id(cls, id):
        return cls.objects(id=id).first()

    def __repr__(self):
        return "<User {}>".format(self.username)


class Device(db.EmbeddedDocument):

    TYPES = {'switch': 1,
             'sensor': 2}

    id = db.ObjectIdField(default=ObjectId)
    port = db.IntField(requiered=True)
    name = db.StringField(max_length=50, requiered=True)
    place = db.StringField(max_length=50, requiered=True)
    type = db.IntField(choices=(1, 2), requiered=True)
    value = db.FloatField(default=0.0)
    is_on = db.BooleanField(default=False)

    def __repr__(self):
        return "<Device> {}".format(self.name)


class Hub(db.Document):
    name = db.StringField(default="HUB-")
    owner = db.ReferenceField(User)
    token = db.StringField(max_length=40, default=secrets.token_urlsafe(30))
    devices = db.EmbeddedDocumentListField(Device)

    def refresh_token(self):
        token = secrets.token_urlsafe(30)
        self.token = token
        self.save()
        return self.token

    @classmethod
    def by_id(cls, id):
        return cls.objects(id=id).first_or_404()

    @classmethod
    def by_owner(cls, owner):
        return cls.objects(owner=owner).all()

    @classmethod
    def by_token(cls, token):
        return cls.objects(token=token).first()

    def add_device(self, device):
        """
        add new device to the hub
        :param device: Device object """
        self.devices.append(device)
        self.save()

    def get_device(self, port):
        """
        :param port: port number
        :returns Device connected to a specific port"""
        return self.devices.filter(port=port).first()
