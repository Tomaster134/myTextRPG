import dill
import itertools


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
    def __init__(self, name, description, position, exits, icon, contents={'NPCs': {}, 'Players': {}, 'Items': {}}) -> None:
        super().__init__(name, description)
        self.id = next(Room.id)
        self.position = position #Coordinates in the grid system for a room, will be used when a character moves rooms
        self.exits = exits #List of rooms that are connected to this room. Should be N,S,E,W but may expand so a player can "move/go shop or someting along those lines"
        self.icon = icon #Icon for the world map, should consist of two ASCII characters (ie: "/\" for a mountain)
        self.contents = contents #Dictionary containing all NPCs, Players, and Items currently in the room. Values will be modified depending on character movement, NPC generation, and item movement

    def describe_contents(self, caller):
        output = ''
        print(f'Room Object: {id(self)}')
        print(f'Room Name: {self.name}')
        print(f'Room Position: {self.position}')
        print(f'Room Contents: {self.contents}')
        return output

room_dict = {
    (0,0): {
        'name': 'Town Square',
        'description': 'This is the center of town! More to come.',
        'position': '0,0',
        'exits': {
            'north': '0,1',
            'south': '0,-1',
            'east': '1,0',
            'west': '-1,0'
        },
        'icon': '()'
    },
    (0,1): {
        'name': 'Pavilion',
        'description': 'There is a pavilion here with two buildings to the east and west.',
        'position': '0,1',
        'exits': {
            'south': '0,0',
            'east': '1,1',
            'west': '-1,1'
        },
        'icon': '/\\'
    },
    (0,-1): {
        'name': 'Gravel Path',
        'description': 'There is a gravel path here, leading to a forest to the east and a lake to the west.',
        'position': '0,-1',
        'exits': {
            'north': '0,0',
            'east': '1,-1',
            'west': '-1,-1'
        },
        'icon': '||'
    },
    (1,0): {
        'name': 'Neighborhood',
        'description': 'There are many houses here. All appear locked.',
        'position': '1,0',
        'exits': {
            'west': '0,0'
        },
        'icon': '_^'
    },
    (-1,0): {
        'name': 'Barracks',
        'description': 'You are in the entrance to the baracks.',
        'position': '-1,0',
        'exits': {
            'east': '0,0'
        },
        'icon': '()'
    },
    (-1,1): {
        'name': 'Mayor\'s House',
        'description': 'You stand before the mayor\'s house. It is opulent and makes you want to rage against the ruling class.',
        'position': '-1,1',
        'exits': {
            'east': '0,1',
        },
        'icon': '^^'
    },
    (1,1): {
        'name': 'General Store',
        'description': 'A small shop that sells various essential goods.',
        'position': '1,1',
        'exits': {
            'west': '0,1'
        },
        'icon': 'oo'
    },
    (1,-1): {
        'name': 'Forest',
        'description': 'A foreboding forest. You feel the trees pressing down above you, and every noise makes you twitch in fear.',
        'position': '1,-1',
        'exits': {
            'west': '0,-1'
        },
        'icon': 'Tt'
    },
    (-1,-1): {
        'name': 'Lake',
        'description': 'A placid lake. You feel at peace here.',
        'position': '-1,-1',
        'exits': {
            'east': '0,-1',
        },
        'icon': '~~'
    }
}

rooms = {}
for room in room_dict.values():
    new_room = Room(room['name'], room['description'], room['position'], room['exits'], room['icon'])
    rooms.update({new_room.position: new_room})
with open('app/data/room_db.pkl', 'wb') as dill_file:
   dill.dump(rooms, dill_file)

# with open('app/data/room_db.pkl', 'rb') as dill_file:
#     rooms = dill.load(dill_file)
# print(rooms)
# print(rooms['0,0'].id, rooms['0,0'].name, rooms['0,0'].description, rooms['0,0'].position, rooms['0,0'].exits, rooms['0,0'].icon, rooms['0,0'].contents)