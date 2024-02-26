from flask import session
from flask_login import current_user
from ... import socketio
from flask_socketio import join_room, leave_room, emit
from .routes import rooms


@socketio.on('connect')
def connect(auth):
    print('connection')
    print(session.get('room'))
    username = session.get('username')
    location = session.get('location')
    join_room(location)
    print(f'joined {location}')
    content = {
    'username': username,
    'message': 'has joined the room',
    'type': 'status'
}
    emit('status', {'username': username, 'message': 'has entered the room'}, room=location)
    print(f'emitted {content} to {location}')

@socketio.on('disconnect')
def disconnect():
    room = session.get('location')
    username = session.get('username')
    current_user.location = session.get('location')
    current_user.save()
    print(f'{current_user} location saved')
    leave_room(room)

    content = {
    'username': username,
    'message': 'has left the room',
    'type': 'status'
}

    emit('status', {'username': username, 'message': 'has left the room'}, room=room)

@socketio.on('say')
def say(data):
    print('message')
    room = session.get('location')
    print(room)
    content = {
        'username': session.get('username'),
        'message': data['data'],
        'type': 'message'
    }

    if data['command'] == 'say':
        emit('message', {'username': content['username'], 'message': content['message']}, room=room)