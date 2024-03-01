from flask import session, request
from flask_login import current_user
from ... import socketio
from flask_socketio import join_room, leave_room, emit
import app.blueprints.main.objects as objects
import dill


#Socket IO events, should only be three. On connection, on disconnect, and whenever data is sent

client_list = [] #List of clients currently connected

#Instatiating world class to hold all rooms, players, and characters

world = objects.World()
#This is an event that occurs whenever a new connection is detected by the socketio server. Connection needs to properly connect the user with their Player object, update the Player object's session_id so private server emits can be transmitted to that player only
@socketio.on('connect')
def connect():
    username = session.get('username')
    location = session.get('location')
    client_list.append(request.sid)
    print(f'client list is {client_list}')
    join_room(location)
    content = {
    'username': username,
    'message': 'has joined the room',
    'type': 'status'
}
    emit('status', {'username': username, 'message': 'has entered the room'}, room=location)

#Event that handles disconnection. Unsure if I should be saving player information on disconnect or periodically. Likely both. Need to remove the player and client from the list of active connections. If all players are disconnected, world state should be saved and server activity spun down.
@socketio.on('disconnect')
def disconnect():
    room = session.get('location')
    username = session.get('username')
    current_user.location = session.get('location')
    current_user.save()
    socketio.sleep(1)
    client_list.pop(client_list.index(request.sid))
    print(f'client list is {client_list}')
    leave_room(room)

    content = {
    'username': username,
    'message': 'has left the room',
    'type': 'status'
}

    emit('status', {'username': username, 'message': 'has left the room'}, room=room)


#This needs to revamped to essentially handle input and properly reroute input to the proper functions and methods
