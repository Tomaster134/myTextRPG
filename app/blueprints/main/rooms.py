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
        'name': 'Mayor\'s Courtyard',
        'description': 'You stand before the mayor\'s house. It is opulent and makes you want to rage against the ruling class.',
        'position': '-1,1',
        'exits': {
            'east': '0,1',
            'in': 'Mayoral Mansion'
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
    },
    'Mayoral Mansion': {
    'name': 'The Mayoral Mansion',
    'description': 'Soaring arches, glass chandeliers, thick rugs. The mayor of this town is clearly not hurting for money.',
    'position': 'Mayoral Mansion',
    'exits': {
        'out': '-1,1',
    },
    'icon': '^^'
    }
}

# rooms = {}
# for room in room_dict.values():
#     new_room = Room(room['name'], room['description'], room['position'], room['exits'], room['icon'])
#     rooms.update({new_room.position: new_room})
# with open('app/data/room_db.pkl', 'wb') as dill_file:
#    dill.dump(rooms, dill_file)

# with open('app/data/room_db.pkl', 'rb') as dill_file:
#     rooms = dill.load(dill_file)
# print(rooms)
# print(rooms['0,0'].id, rooms['0,0'].name, rooms['0,0'].description, rooms['0,0'].position, rooms['0,0'].exits, rooms['0,0'].icon, rooms['0,0'].contents)