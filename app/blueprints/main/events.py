from flask import session
from flask_login import login_required
from . import main
from ... import socketio
from flask_socketio import join_room, leave_room, emit
from .routes import rooms

@socketio.on('connect')
def joined(auth):
    print('connection')
    print(session.get('room'))
    room = session.get('room')
    username = session.get('username')
    if not room or not username:
        print('not room')
        return
    if room not in rooms:
        print('room not in rooms')
        leave_room(room)
        return
    join_room(room)
    print(f'joined {room}')
    content = {
    'username': username,
    'message': 'has joined the room',
    'type': 'status'
}
    emit('status', {'username': username, 'message': 'has entered the room'}, room=room)
    print(f'emitted {content} to {room}')
    rooms[room]['members'] += 1
    rooms[room]['messages'].append(content)

@socketio.on('disconnect')
def left():
    room = session.get('room')
    username = session.get('username')
    leave_room(room)
    if room in rooms:
        rooms[room]['members'] -= 1

    content = {
    'username': username,
    'message': 'has left the room',
    'type': 'status'
}

    emit('status', {'username': username, 'message': 'has left the room'}, room=room)
    rooms[room]['messages'].append(content)

@socketio.on('message')
def message(data):
    print('message')
    room = session.get('room')
    if room not in rooms:
        return
    payload = {}
    payload['command'] = data['data'].split(maxsplit=1)[0]
    payload['data'] = data['data'].split(maxsplit=1)[1]
 
    content = {
        'username': session.get('username'),
        'message': payload['data'],
        'type': 'message'
    }

    if payload['command'] == 'say':
        emit('message', {'username': content['username'], 'message': content['message']}, room=room)
        rooms[room]['messages'].append(content)