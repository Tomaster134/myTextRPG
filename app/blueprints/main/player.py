from flask import session
from flask_login import login_required
from ... import socketio
from flask_socketio import join_room, leave_room, emit


# Might need this? Unsure.

class TestPlayer ():
    def __init__(self, name) -> None:
        self.name = name
        self.health = 100

    def describe(self):
        print('describe has been called')
        return f'they have {self.health} health'
    
    def damage(self):
        self.health -= 10
        print('damage has been called')