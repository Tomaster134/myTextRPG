import shelve
#Overall class for any interactable object in the world
class Entity():
    def __init__(self, id, name, description) -> None:
        self.id = id #Every entity needs a unique identifier
        self.name = name #Shorthand name for each entity
        self.description = description #Every entity needs to be able to be looked at


#Class for rooms. Rooms should contain all other objects (NPCs, Items, Players, anything else that gets added)
class Room(Entity):
    def __init__(self, id, name, description, position, exits, icon, contents={'NPCs': [], 'Players': [], 'Items': []}) -> None:
        super().__init__(id, name, description)
        self.position = position #Coordinates in the grid system for a room, will be used when a character moves rooms
        self.exits = exits #List of rooms that are connected to this room. Should be N,S,E,W but may expand so a player can "move/go shop or someting along those lines"
        self.icon = icon #Icon for the world map, should consist of two ASCII characters (ie: "/\" for a mountain)
        self.contents = contents #Dictionary containing all NPCs, Players, and Items currently in the room. Values will be modified depending on character movement, NPC generation, and item movement
room_dict = {
    (0,0): {
        'id': 1,
        'name': 'Town Square',
        'description': 'This is the center of town! More to come.',
        'position': '(0,0)',
        'exits': {
            'north': '(0,1)',
            'south': '(0,-1)',
            'east': '(1, 0)',
            'west': '(-1, 0)'
        },
        'icon': '()'
    },
    (0,1): {
        'id': 2,
        'name': 'Pavilion',
        'description': 'There is a pavilion here with two buildings to the east and west.',
        'position': '(0,1)',
        'exits': {
            'south': '(0,0)',
            'east': '(1, 1)',
            'west': '(-1, 1)'
        },
        'icon': '/\\'
    },
    (0,-1): {
        'id': 3,
        'name': 'Gravel Path',
        'description': 'There is a gravel path here, leading to a forest to the east and a lake to the west.',
        'position': '(0,-1)',
        'exits': {
            'north': '(0,0)',
            'east': '(1, -1)',
            'west': '(-1, 1)'
        },
        'icon': '||'
    },
    (1,0): {
        'id': 4,
        'name': 'Neighborhood',
        'description': 'There are many houses here. All appear locked.',
        'position': '(1,0)',
        'exits': {
            'west': '(0, 0)'
        },
        'icon': '_^'
    },
    (-1,0): {
        'id': 5,
        'name': 'Barracks',
        'description': 'You are in the entrance to the baracks.',
        'position': '(-1,0)',
        'exits': {
            'east': '(0, 0)'
        },
        'icon': '()'
    },
    (-1,1): {
        'id': 6,
        'name': 'Mayor\'s House',
        'description': 'You stand before the mayor\'s house. It is opulent and makes you want to rage against the ruling class.',
        'position': '(-1,1)',
        'exits': {
            'east': '(0,1)',
        },
        'icon': '^^'
    },
    (1,1): {
        'id': 7,
        'name': 'General Store',
        'description': 'A small shop that sells various essential goods.',
        'position': '(1,1)',
        'exits': {
            'west': '(0,1)'
        },
        'icon': 'oo'
    },
    (1,-1): {
        'id': 8,
        'name': 'Forest',
        'description': 'A foreboding forest. You feel the trees pressing down above you, and every noise makes you twitch in fear.',
        'position': '(1,-1)',
        'exits': {
            'west': '(0,-1)'
        },
        'icon': 'Tt'
    },
    (-1,-1): {
        'id': 9,
        'name': 'Lake',
        'description': 'A placid lake. You feel at peace here.',
        'position': '(-1,-1)',
        'exits': {
            'east': '(0,-1)',
        },
        'icon': '~~'
    }
}

room_db = shelve.open('app/data/rooms')
rooms = []
for room in room_dict.values():
    room_db[str(room['id'])] = Room(room['id'], room['name'], room['description'], room['position'], room['exits'], room['icon'])
room_db.close()