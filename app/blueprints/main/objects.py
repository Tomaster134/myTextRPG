from ... import socketio
from flask import request
import app.blueprints.main.events as events
import dill
import itertools
from flask_socketio import join_room, leave_room
import app.blueprints.main.rooms as room_file

#World class that holds all entities
class World():
    def __init__(self) -> None:
        rooms = {}
        for room in room_file.room_dict.values():
            new_room = Room(room['name'], room['description'], room['position'], room['exits'], room['icon'])
            rooms.update({new_room.position: new_room})
        self.rooms = rooms
        self.players = {}

    def world_test(self):
        for room in self.rooms.values():
            print(id(room), room.name, room.contents)

    #Might not use this, and instead use individual pickles for each entity type for modularization
    # def world_save(self):
    #     with open('app/data/world_db.pkl', 'wb') as dill_file:
    #         dill.dump(self, dill_file)
    #     socketio.emit('event', {'message': 'world saved'})

    # def room_save(self):
    #     with open('app/data/room_db.pkl', 'wb') as dill_file:
    #         dill.dump(self.rooms, dill_file)
    #     socketio.emit('event', {'message': 'rooms saved'})


#Overall class for any interactable object in the world
class Entity():
    def __init__(self, name, description) -> None:
        self.name = name #Shorthand name for an entity
        self.description = description #Every entity needs to be able to be looked at

    #Test function currently, but every entity needs to be able to describe itself when looked at
    def describe(self):
        pass

#Class for rooms. Rooms should contain all other objects (NPCs, Items, Players, anything else that gets added)
class Room(Entity):
    id = itertools.count()
    def __init__(self, name, description, position, exits, icon) -> None:
        super().__init__(name, description)
        self.id = next(Room.id)
        self.position = position #Coordinates in the grid system for a room, will be used when a character moves rooms
        self.exits = exits #List of rooms that are connected to this room. Should be N,S,E,W but may expand so a player can "move/go shop or someting along those lines"
        self.icon = icon #Icon for the world map, should consist of two ASCII characters (ie: "/\" for a mountain)
        self.contents = {'NPCs': {}, 'Players': {}, 'Items': {}} #Dictionary containing all NPCs, Players, and Items currently in the room. Values will be modified depending on character movement, NPC generation, and item movement

    def describe_contents(self, caller):
        output = ''
        player_list = dict(self.contents['Players'])
        del player_list[caller.id]
        player_key = list(enumerate(player_list))
        if len(player_list) == 0:
            pass
        elif len(player_list) == 1:
            socketio.emit('event', {'message': f'{player_list[player_key[0][1]].name} stands here.'}, to=caller.session_id)
        elif len(player_list) == 2:
            socketio.emit('event', {'message': f'{player_list[player_key[0][1]].name} and {player_list[player_key[1][1]].name} stand here.'}, to=caller.session_id)
        else:
            for i in range(len(player_list)):
                if i == len(player_list)-1:
                    output += f'and {player_list[player_key[i][1]].name} stand here.'
                else: output += f'{player_list[player_key[i][1]].name}, '
            socketio.emit('event', {'message': output}, to=caller.session_id)


#Broad class for any entity capable of independent and autonomous action that affects the world in some way
default_stats = {
'strength': 10,
'endurance': 10,
'intelligence': 10,
'wisdom': 10,
'charisma': 10,
'agility': 10
}
class Character(Entity):
    def __init__(self, name, description, health=100, level=1, location='0,0', stats=default_stats, deceased=False) -> None:
        super().__init__(name, description)
        self.health = health #All characters should have a health value
        self.level = level #All characters should have a level value
        self.location = location #All characters should have a location, reflecting their current room and referenced when moving
        self.stats = stats #All characters should have a stat block.
        self.deceased = deceased #Indicator of if a character is alive or not. If True, inventory can be looted
        self.inventory = [] #List of items in character's inventory. May swap to a dictionary of lists so items can be placed in categories


#Class that users control to interact with the world. Unsure if I need to have this mixed in with the models side or if it would be easier to pickle the entire class and pass that to the database?
class Player(Character):
    def __init__(self, id, account, name, description, health=100, level=1, location='0,0', stats=default_stats, deceased=False) -> None:
        super().__init__(name, description, health, level, location, stats, deceased)
        self.id = id
        self.account = account #User account associated with the player character
        self.session_id = '' #Session ID so messages can be broadcast to players without other members of a room or server seeing the message. Session ID is unique to every connection, so part of the connection process must be to assign the new value to the player's session_id
        self.inventory = []

    def connection(self):
        events.world.rooms[self.location].contents['Players'].update({self.id: self})

    def disconnection(self):
        del events.world.rooms[self.location].contents['Players'][self.id]

    def look(self, data, room):
        if data == '':
            socketio.emit('event', {'message': self.location}, to=self.session_id)
            socketio.emit('event', {'message': room.description}, to=self.session_id)
            room.describe_contents(self)
        else:
            socketio.emit('event', {'message': 'this will eventually be a call to a class\'s .description to return a look statement.'}, to=self.session_id)
    
    def speak(self, data):
        socketio.emit('event', {'message': f'{self.name} says "{data}"'}, room=self.location, include_self=False)
        socketio.emit('event', {'message': f'You say "{data}"'}, to=self.session_id)

    def move(self, direction, room):
        if direction not in room.exits:
            socketio.emit('event', {'message': 'You can\'t go that way.'}, to=self.session_id)
            return
        leave_room(self.location)
        socketio.emit('event', {'message': f'{self.name} moves towards the {direction}'}, room=self.location)
        if self.id in room.contents['Players']:
            del room.contents['Players'][self.id]


        lat = int(self.location[:self.location.index(',')])
        lon = int(self.location[self.location.index(',')+1:])
        if direction == 'n' or direction == 'north':
            lon += 1
            socketio.emit('event', {'message': 'You move towards the north'}, to=self.session_id)
        if direction == 's' or direction == 'south':
            lon -= 1
            socketio.emit('event', {'message': 'You move towards the south'}, to=self.session_id)
        if direction == 'e' or direction == 'east':
            lat += 1
            socketio.emit('event', {'message': 'You move towards the east'}, to=self.session_id)
        if direction == 'w' or direction == 'west':
            lat -= 1
            socketio.emit('event', {'message': 'You move towards the west'}, to=self.session_id)

        new_location = f'{lat},{lon}'
        came_from = [i for i in events.world.rooms[new_location].exits if events.world.rooms[new_location].exits[i]==self.location]
        socketio.emit('event', {'message': f'{self.name} arrives from the {came_from[0]}'}, room=new_location)
        socketio.sleep(.5)
        self.location = new_location
        join_room(self.location)
        events.world.rooms[self.location].contents['Players'].update({self.id: self})
        socketio.emit('event', {'message': events.world.rooms[self.location].description}, to=self.session_id)
        events.world.rooms[self.location].describe_contents(self)

#Class that is controlled by the server. Capable of being interacted with.
class NPC(Character):
    id = itertools.count()
    def __init__(self, name, description, deceased, health, level, location, home, stats) -> None:
        super().__init__(name, description, deceased, health, level, location, stats)
        self.id = next(NPC.id)
        self.home = home #Spawn location if NPC is killed. Can also double as a bound to prevent NPC from wandering too far from home during world timer movement
        self.inventory = []

#Class that is incapable of autonomous action. Inanimate objects and such.
class Item(Entity):
    id = itertools.count()
    def __init__(self, name, description, group, weight, equippable=False) -> None:
        super().__init__(name, description)
        self.id = next(Item.id)
        self.group = group #Type of item. Food, equipment, quest, etc
        self.weight = weight #Weight of item. Will be used alongside character strength to determine if the item can be picked up, pulled to inventory, etc
        self.equippable = equippable #Can you equip the item. Unsure if redundant with equipment class

#Subclass of items that is capable of being equipped by the Character class
class Equipment(Item):
    def __init__(self, name, description, group, weight, category, equippable) -> None:
        super().__init__(name, description, group, weight, equippable)
        self.equippable = True #All equipment should be equippable
        self.category = category #Further granularity with group. Is the equipment armor, clothing, sword, axe, etc. Unsure if I should instead make child classes of equipment instead so I can dictate specific stat blocks