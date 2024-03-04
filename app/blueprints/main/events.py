from flask import session, request
from flask_login import current_user
from ... import socketio
from flask_socketio import join_room, leave_room, emit
from app.models import PlayerAccount, User
import app.blueprints.main.objects as objects
import dill


#Socket IO events, should only be three. On connection, on disconnect, and whenever data is sent

client_list = [] #List of clients currently connected

#Instatiating world class to hold all rooms, players, and characters

world = objects.World()
#This is an event that occurs whenever a new connection is detected by the socketio server. Connection needs to properly connect the user with their Player object, update the Player object's session_id so private server emits can be transmitted to that player only
@socketio.on('connect')
def connect():
    active_player = current_user.accounts.filter(PlayerAccount.is_active == True).first() #Pulls the active player information
    if not active_player.player_info: #Checks to see if the active player is a new player
        player = objects.Player(id=active_player.id, name=active_player.player_name, description="A newborn player, fresh to the world.", account=active_player.user_id)
        print(f'id = {player.id}, name = {player.name}, description = {player.description}, health = {player.health}, level = {player.level}, stats = {player.stats}, location = {player.location}, inventory = {player.inventory}') #Creates a new player object
        active_player.player_info = dill.dumps(player) #Pickles and writes new player object to active player info
        print(active_player.player_info)
        active_player.save() #Saves pickled data to player database
    else:
        player = dill.loads(active_player.player_info) #Loads pickled data in to the player
        print(player.name)
    username = player.name
    location = player.location
    player.session_id = request.sid
    client_list.append(player.session_id)
    world.players.update({player.id: player})
    print(f'client list is {client_list}')
    print(f'players connected is {world.players}')
    session['player_id'] = player.id
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
    player_id = session.get('player_id')
    player = PlayerAccount.query.get(player_id)
    room = session.get('location')
    username = session.get('username')
    current_user.location = session.get('location')
    current_user.save()
    socketio.sleep(1)
    client_list.pop(client_list.index(request.sid))
    player.player_info = dill.dumps(world.players[player_id])
    player.save()
    del world.players[player_id]
    print(f'connected players: {world.players}')
    print(f'client list is {client_list}')
    leave_room(room)

    content = {
    'username': username,
    'message': 'has left the room',
    'type': 'status'
}

    emit('status', {'username': username, 'message': 'has left the room'}, room=room)


#This needs to revamped to essentially handle input and properly reroute input to the proper functions and methods
