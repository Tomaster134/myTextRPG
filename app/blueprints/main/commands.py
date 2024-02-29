from flask import session, request
from flask_login import current_user
from ... import socketio
from flask_socketio import join_room, leave_room, emit
from . import events

#List of commands, needs to be revamped into class methods, with the socketio event calling a broad function depending on the information passed through from the client, and the function calling a class method. Unsure if i can cut out the middle man function


#This event should be moved to the Character class and using their move method
@socketio.event
def move(data):
    print(f'session ID is {request.sid}')
    print(f'leaving room {session["location"]}')
    location = session['location']
    username = session['username']
    sid = request.sid
    print(username)
    leave_room(location)
    socketio.emit('status', {'username': username, 'message': 'walks out of the room'}, room=location)
    lat = int(location[:location.index(',')])
    lon = int(location[location.index(',')+1:])
    print(f'lat is {lat}, lon is {lon}')
    if data['data'] == 'n' or data['data'] == 'north':
        lat += 1
        emit('look', {'message': 'You move towards the north'}, room=sid)
    if data['data'] == 's' or data['data'] == 'south':
        lat -= 1
        emit('look', {'message': 'You move towards the south'}, room=sid)
    if data['data'] == 'e' or data['data'] == 'east':
        lon += 1
        emit('look', {'message': 'You move towards the east'}, room=sid)
    if data['data'] == 'w' or data['data'] == 'west':
        lon -= 1
        emit('look', {'message': 'You move towards the west'}, room=sid)
    session['location'] = f'{lat},{lon}'
    print(f'new lat is {lat}, new lon is {lon}')
    print(f'current room is {session["location"]}')
    location = session['location']
    socketio.emit('status', {'username': username, 'message': 'walks into the room'}, room=location)
    join_room(session['location'])

#This event should be moved to the Player class and using their look method
@socketio.event
def look(data):
    sid = request.sid
    if data['data'] == '':
        location = session['location']
        emit('look', {'message': location}, to=sid)
    else:
        emit('look', {'message': 'this will eventually be a call to a class\'s .description to return a look statement.'}, to=sid)

#These are primarily test functions to make sure the world timer is functional
@socketio.event
def test(data):
    sid = request.sid
    print('this is a test confirming receipt')
    session.get('player_list')[0].describe()

@socketio.event
def attack(data):
    sid = request.sid
    session.get('player_list')[0].damage()
    emit('look', {'message': 'You hit the test for 10 damage'})