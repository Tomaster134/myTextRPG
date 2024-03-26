from flask import session, request
from ... import socketio
from flask_socketio import join_room, leave_room, emit
from app.models import PlayerAccount, User
import app.blueprints.main.objects as objects
import dill


#Socket IO events, should only be three. On connection, on disconnect, and whenever data is sent
client_list = [] #List of clients currently connected
world = objects.World() #Instatiating world class to hold all rooms, players, and characters

def world_timer():
     print('world timer triggered')
     socketio.sleep(10)
     while True:
            print('world timer active')
            if client_list:
                socketio.sleep(10)
                for character in world.npcs.values():
                     character.ambiance()
                for room in world.rooms.values():
                     room.ambiance()
            else: break


#This is an event that occurs whenever a new connection is detected by the socketio server. Connection needs to properly connect the user with their Player object, update the Player object's session_id so private server emits can be transmitted to that player only
@socketio.on('connect')
def connect(auth):
    session['user_id'] = auth
    print(session['user_id'])
    current_user = User.query.filter(User.id == auth).first()
    active_player = current_user.accounts.filter(PlayerAccount.is_active == True).first() #Pulls the active player information
    if not active_player.player_info: #Checks to see if the active player is a new player
        player = objects.Player(id=active_player.id, name=active_player.player_name, description="A newborn player, fresh to the world.", account=active_player.user_id)
        #Creates a new player object
        active_player.player_info = dill.dumps(player) #Pickles and writes new player object to active player info
        active_player.save() #Saves pickled data to player database
    else:
        player = dill.loads(active_player.player_info, ignore=False) #Loads pickled data in to the player
    username = player.name
    location = player.location
    player.session_id = request.sid
    client_list.append(player.session_id)
    world.players.update({player.id: player})
    if client_list:
        socketio.start_background_task(world_timer)
    print(f'client list is {client_list}')
    print(f'players connected is {world.players}')
    session['player_id'] = player.id
    session['player'] = player
    join_room(location)
    player.location_map()
    socketio.emit('event', {'message': f'{username} has connected to the server'})
    player.connection()

#Event that handles disconnection. Unsure if I should be saving player information on disconnect or periodically. Likely both. Need to remove the player and client from the list of active connections. If all players are disconnected, world state should be saved and server activity spun down.
@socketio.on('disconnect')
def disconnect():
    player_id = int(session['player_id'])
    player_account = PlayerAccount.query.get(player_id)
    player = world.players[player_id]
    room = player.location
    client_list.pop(client_list.index(player.session_id))
    player_account.player_info = dill.dumps(player)
    player_account.save()
    del world.players[player_id]
    leave_room(room)
    player.disconnection()
    socketio.emit('event', {'message': f'{player.name} has left the server'})


#This needs to revamped to essentially handle input and properly reroute input to the proper functions and methods
