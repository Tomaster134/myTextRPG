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
    active_account = db.Column(db.Integer)
    accounts = db.relationship('PlayerAccount',
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

class PlayerAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    player_name = db.Column(db.String, unique=True)
    player_info = db.Column(db.LargeBinary)
    is_active = db.Column(db.Boolean)

    def __init__(self, user_id, player_name, player_info=None, is_active=False):
        self.user_id = user_id
        self.player_name = player_name
        self.player_info = player_info
        self.is_active = is_active

    def save(self):
        db.session.add(self)
        db.session.commit()