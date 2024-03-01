from flask import session, request
from flask_login import current_user
from ... import socketio
from flask_socketio import join_room, leave_room, emit
import app.blueprints.main.events as events

#List of commands, needs to be revamped into class methods, with the socketio event calling a broad function depending on the information passed through from the client, and the function calling a class method. Unsure if i can cut out the middle man function

@socketio.event
def client(data):
    content = {
        'player': session.get('username'),
        'sid': request.sid,
        'location': session.get('location'),
        'command': data['command'],
        'data': data['data'],
    }

    if content['command'] == 'say':
        say(content['player'], content['sid'], content['location'], content['data'])

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
        move(content['player'], content['sid'], content['location'], content['data'])

    if data['command'] == 'look' or data['command'] == 'l':
        look(content['player'], content['sid'], content['location'], content['data'])



#This event should be moved to the Character class and using their move method
        
def say(player, sid, location, data):
    emit('event', {'message': f'{player} says "{data}"'}, room=location, include_self=False)
    emit('event', {'message': f'You say "{data}"'}, to=sid)

def move(player, sid, location, direction):
    if direction not in events.world.rooms[location].exits:
        emit('event', {'message': 'You can\'t go that way.'}, to=sid)
        return
    leave_room(location)
    socketio.emit('event', {'message': f'{player} moves towards the {direction}'}, room=location)

    lat = int(location[:location.index(',')])
    lon = int(location[location.index(',')+1:])
    if direction == 'n' or direction == 'north':
        lon += 1
        emit('event', {'message': 'You move towards the north'}, to=sid)
    if direction == 's' or direction == 'south':
        lon -= 1
        emit('event', {'message': 'You move towards the south'}, to=sid)
    if direction == 'e' or direction == 'east':
        lat += 1
        emit('event', {'message': 'You move towards the east'}, to=sid)
    if direction == 'w' or direction == 'west':
        lat -= 1
        emit('event', {'message': 'You move towards the west'}, to=sid)

    session['location'] = f'{lat},{lon}'
    new_location = session['location']
    came_from = [i for i in events.world.rooms[new_location].exits if events.world.rooms[new_location].exits[i]==location]
    socketio.emit('event', {'message': f'{player} arrives from the {came_from[0]}'}, room=new_location)
    socketio.sleep(.5)
    join_room(session['location'])
    emit('event', {'message': events.world.rooms[new_location].description}, to=sid)

#This event should be moved to the Player class and using their look method
def look(player, sid, location, data=''):
    if data == '':
        emit('event', {'message': location}, to=sid)
        emit('event', {'message': events.world.rooms[location].description}, to=sid)
    else:
        emit('event', {'message': 'this will eventually be a call to a class\'s .description to return a look statement.'}, to=sid)

#These are primarily test functions to make sure the world timer is functional
@socketio.event
def test(data):
    sid = request.sid
    events.world.world_test()

@socketio.event
def attack(data):
    sid = request.sid

@socketio.event
def save(data):
    events.world.save()