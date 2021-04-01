from app import db
from app.commons import APP_NAME
from app.API.utils import set_switch_state
from mongoengine.errors import NotUniqueError, ValidationError
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
import secrets


class RevokedToken(db.Document):
    jti = db.StringField(unique=True)

    @classmethod
    def is_blacklisted(cls, jti):
        return cls.objects(jti=jti).first() != None

    @classmethod
    def add(cls, jti):
        return cls(jti=jti).save()


class User(db.Document):
    email = db.EmailField(max_length=50, unique=True)
    username = db.StringField(max_length=50, unique=True)
    password_hash = db.StringField(max_length=128)
    mqtt_username = db.StringField(max_length=128)
    mqtt_password = db.StringField(max_length=128)
    topics = db.ListField(db.StringField())

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def validate_mqtt(self, mqtt_username, mqtt_password):
        if self.mqtt_username == mqtt_username and \
            self.mqtt_password == mqtt_password:
            return True
    def has_topic(self, topic):
        return topic in self.topics

    def generate_token(self):
        token = create_access_token(identity= {
            "username": self.username,
            "id": str(self.id)
        })
        
        return token


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
    def get_by_username(cls, username):
        return cls.objects(username=username).first()

    @classmethod
    def get_by_id(cls, id):
        return cls.objects(id=id).first()

    @classmethod
    def get_by_mqtt_username(cls, mqtt_username):
        return cls.objects(mqtt_username=mqtt_username).first()

    
    
    def __repr__(self):
        return "<User {}>".format(self.username)


class Device(db.Document):
    TYPES = {'switch': 1,
             'sensor': 2}

    key = db.StringField(unique=True, default=lambda: secrets.token_urlsafe(10))
    owner = db.ReferenceField(User, required=True, reverse_delete_rule="cascade")
    port = db.IntField(requiered=True)
    name = db.StringField(max_length=50, required=True)
    place = db.StringField(max_length=50, required=True)
    d_type = db.StringField(choices=("switch", "sensor"), required=True)
    topic = db.StringField(unique=True)

    def save(self, force_insert=False, validate=True, clean=True, write_concern=None, cascade=None, cascade_kwargs=None,
             _refs=None, save_condition=None, signal_kwargs=None, **kwargs):
    # TODO: elimnate the mqtt dependency by using a queue or smth
        self.topic = self._generate_topic()    
        # tell the broker to set the switch to 0
        flag = True
        if self.d_type == "switch":
            flag = set_switch_state(self, "0") 
        if not flag:
            raise Exception("MQTT Failure")  
        # update user topics 
        self.owner.topics.append(self.topic)
        self.owner.save()
        return super().save(force_insert, validate, clean, write_concern, cascade, cascade_kwargs, _refs,
                        save_condition, signal_kwargs, **kwargs)

    def delete(self, signal_kwargs=None, **write_concern):
        self.owner.topics.remove(self.topic)
        self.owner.save()
        return super().delete(signal_kwargs, **write_concern)

    def _generate_topic(self):
        _TOPIC_TEMP = APP_NAME + "/{username}/{key}/{d_type}/{port}"
        return _TOPIC_TEMP.format(username=self.owner.username, key=self.key, d_type=self.d_type, port=self.port)

    def serialize(self):
        return {
            "key": self.key,
            "user_id": str(self.owner.id),
            "name": self.name,
            "place": self.place,
            "type": self.d_type,
            "port": self.port,
            "topic": self.topic
        }
    @classmethod
    def by_owner(cls, owner):
        return cls.objects(owner=owner).all()

    @classmethod
    def by_key(cls, key):
        return cls.objects(key=key).first()

    def __repr__(self):
        return "<Device> {}".format(self.name)
