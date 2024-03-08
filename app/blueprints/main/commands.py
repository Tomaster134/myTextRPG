from flask import session, request
from flask_login import current_user
from ... import socketio
from flask_socketio import join_room, leave_room, emit
import app.blueprints.main.events as events

#List of commands, needs to be revamped into class methods, with the socketio event calling a broad function depending on the information passed through from the client, and the function calling a class method. Unsure if i can cut out the middle man function


@socketio.event
def client(data):
    current_player = events.world.players[session.get('player_id')]
    current_room = events.world.rooms[current_player.location]
    content = {
        'player': current_player,
        'room': current_room,
        'command': data['command'],
        'data': data['data'],
    }

    if content['command'] == 'say':
        say(content['player'], content['data'])

    if content['command'] in ['move', 'go', 'north', 'south', 'east', 'west', 'n', 's', 'e', 'w']:
        if not content['data']:
            content['data'] = content['command']
        if content['data'] == 'n':
            content['data'] = 'north'
        if content['data'] == 's':
            content['data'] = 'south'
        if content['data'] == 'e':
            content['data'] = 'east'
        if content['data'] == 'w':
            content['data'] = 'west'
        move(player=content['player'], direction=content['data'], room=content['room'])

    if content['command'] == 'look' or content['command'] == 'l':
        look(player=content['player'], data=content['data'], room=content['room'])

    if content['command'] == 'test':
        test(content['player'], content['data'])

    if content['command'] == 'save':
        save(content['player'], content['data'])



#This event should be moved to the Character class and using their move method
        
def say(player, data):
    player.speak(data)

def move(player, direction, room):
    player.move(direction=direction, room=room)

#This event should be moved to the Player class and using their look method
def look(player, room, data=''):
    player.look(data=data, room=room)

#These are primarily test functions to make sure the world timer is functional
def test(player, data):
    events.world.world_test()

def save(player, player_id, sid, location, data):
    events.world.world_save()
    events.world.room_save()