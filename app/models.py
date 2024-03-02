from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, unique=True)
    location = db.Column(db.String)
    accounts = db.relationship('Player',
                             backref = 'played_by',
                             lazy = 'dynamic')

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        self.location = '0,0'

    def save(self):
        db.session.add(self)
        db.session.commit()

class Player (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    username = db.Column(db.String)
    level = db.Column(db.Integer)
    health = db.Column(db.Integer)
    strength = db.Column(db.Integer)
    endurance = db.Column(db.Integer)
    intelligence = db.Column(db.Integer)
    agility = db.Column(db.Integer)
    perception = db.Column(db.Integer)
    charisma = db.Column(db.Integer)
    location = db.Column(db.String)

    def __init__(self, username, user_id, location='0,0'):
        self.username = username
        self.user_id = user_id
        self.level = 1
        self.health = 100
        self.strength = 10
        self.endurance = 10
        self.intelligence = 10
        self.agility = 10
        self.perception = 10
        self.charisma = 10
        self.location = location
        self.alive = True

    def save(self):
        db.session.add(self)
        db.session.commit()