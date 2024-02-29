from ... import socketio
from flask import request
import app.blueprints.main.events as events
import dill

#World class that holds all entities
class World():
    def __init__(self) -> None:
        rooms = []
        dill_file = open('app/data/room_db.pkl', 'rb')
        rooms = dill.load(dill_file)
        self.rooms = rooms
        print(f'World initialized with {self.rooms}')

    def world_test(self):
        print('world initalized')
        socketio.emit('look', {'message': self.rooms[0].description})

#Overall class for any interactable object in the world
class Entity():
    def __init__(self, id, description) -> None:
        self.id = id #Every entity needs a unique identifier
        self.description = description #Every entity needs to be able to be looked at

    #Test function currently, but every entity needs to be able to describe itself when looked at
    def describe(self):
        print(f'this is entity {self.id} describing itself')
        print(f'this is the request sid {events.client_list}')
        socketio.emit('look', {'message': self.description})

#Class for rooms. Rooms should contain all other objects (NPCs, Items, Players, anything else that gets added)
class Room(Entity):
    def __init__(self, id, description, position, exits, icon, contents={'NPCs': [], 'Players': [], 'Items': []}) -> None:
        super().__init__(id, description)
        self.position = position #Coordinates in the grid system for a room, will be used when a character moves rooms
        self.exits = exits #List of rooms that are connected to this room. Should be N,S,E,W but may expand so a player can "move/go shop or someting along those lines"
        self.icon = icon #Icon for the world map, should consist of two ASCII characters (ie: "/\" for a mountain)
        self.contents = contents #Dictionary containing all NPCs, Players, and Items currently in the room. Values will be modified depending on character movement, NPC generation, and item movement

#Broad class for any entity capable of independent and autonomous action that affects the world in some way
class Character(Entity):
    def __init__(self, id, description, health, level, location, stats, deceased=False, inventory = []) -> None:
        super().__init__(id, description)
        self.health = health #All characters should have a health value
        self.level = level #All characters should have a level value
        self.location = location #All characters should have a location, reflecting their current room and referenced when moving
        self.stats = stats #All characters should have a stat block.
        self.deceased = deceased #Indicator of if a character is alive or not. If True, inventory can be looted
        self.inventory = inventory #List of items in character's inventory. May swap to a dictionary of lists so items can be placed in categories

#Class that users control to interact with the world. Unsure if I need to have this mixed in with the models side or if it would be easier to pickle the entire class and pass that to the database?
class Player(Character):
    def __init__(self, id, description, health, level, location, stats, account, session_id, inventory=[]) -> None:
        super().__init__(id, description, health, level, location, stats, inventory)
        self.account = account #User account associated with the player character
        self.session_id = session_id #Session ID so messages can be broadcast to players without other members of a room or server seeing the message. Session ID is unique to every connection, so part of the connection process must be to assign the new value to the player's session_id

#Class that is controlled by the server. Capable of being interacted with.
class NPC(Character):
    def __init__(self, id, description, health, level, location, home, stats, inventory=[]) -> None:
        super().__init__(id, description, health, level, location, stats, inventory)
        self.home = home #Spawn location if NPC is killed. Can also double as a bound to prevent NPC from wandering too far from home during world timer movement

#Class that is incapable of autonomous action. Inanimate objects and such.
class Item(Entity):
    def __init__(self, id, description, group, weight, equippable=False) -> None:
        super().__init__(id, description)
        self.group = group #Type of item. Food, equipment, quest, etc
        self.weight = weight #Weight of item. Will be used alongside character strength to determine if the item can be picked up, pulled to inventory, etc
        self.equippable = equippable #Can you equip the item. Unsure if redundant with equipment class

#Subclass of items that is capable of being equipped by the Character class
class Equipment(Item):
    def __init__(self, id, description, group, weight, category, equippable) -> None:
        super().__init__(id, description, group, weight, equippable)
        self.equippable = True #All equipment should be equippable
        self.category = category #Further granularity with group. Is the equipment armor, clothing, sword, axe, etc. Unsure if I should instead make child classes of equipment instead so I can dictate specific stat blocks