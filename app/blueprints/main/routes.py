from flask import request, render_template, redirect, url_for, session, flash
from flask_login import login_required
from . import main
from ... import socketio
from flask_socketio import join_room, leave_room, emit
import random
from string import ascii_uppercase

rooms = {}

def gen_code(length):
    while True:
        code = ''
        for i in range(length):
            code += random.choice(ascii_uppercase)
        if code not in rooms:
            break
    return code

@main.route('/', methods=['POST', 'GET'])
def index():
    # session.clear()
    if request.method == 'POST':
        username = request.form.get('username')
        room_code = request.form.get('room')
        join = request.form.get('join', False)
        create = request.form.get('create', False)

        if not username:
            flash('Put a name in, bubs', 'error')
            return render_template('index.html', username=username, room_code=room_code)
        
        if join != False and not room_code:
            flash('Enter a room code, bubs', 'error')
            return render_template('index.html', username=username, room_code=room_code)
        
        room = room_code

        if create != False:
            if room not in rooms:
                room = (0,0)
                rooms[room] = {'members': 0, "messages": []}
        elif room_code not in rooms:
            flash('Room doesn\'t exist, bubs', 'error')
            return render_template('index.html', username=username, room_code=room_code)
        
        session["room"] = room
        session["username"] = username
        return redirect(url_for('main.room'))

    else: return render_template('index.html')

# @login_required
@main.route('/room')
def room():
    room = session.get('room')
    print(f'room route is {room}')
    return render_template('room.html', room=room, messages=rooms[room]['messages'])