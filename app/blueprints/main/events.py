from flask import session, request
from flask_login import current_user
from ... import socketio
from flask_socketio import join_room, leave_room, emit
from .player import TestPlayer

new_player = TestPlayer('test')
player_list = []
player_list.append(new_player)
session_player_list = tuple(player_list)
print(session_player_list)
client_list = []

@socketio.on('connect')
def connect():
    print('connection')
    username = session.get('username')
    location = session.get('location')
    client_list.append(request.sid)
    print(f'client list is {client_list}')
    session['player_list'] = session_player_list
    join_room(location)
    print(f'joined {location}')
    content = {
    'username': username,
    'message': 'has joined the room',
    'type': 'status'
}
    emit('status', {'username': username, 'message': 'has entered the room'}, room=location)
    print(f'emitted {content} to {location}')
    print(session['player_list'])

@socketio.on('disconnect')
def disconnect():
    room = session.get('location')
    username = session.get('username')
    current_user.location = session.get('location')
    current_user.save()
    print(f'{current_user} location saved')
    client_list.pop(client_list.index(request.sid))
    print(f'client list is {client_list}')
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