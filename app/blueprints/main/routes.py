from flask import request, render_template, redirect, url_for, session, flash
from flask_login import login_required
from . import main
from ... import socketio
from flask_socketio import join_room, leave_room, send, emit
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
            room = gen_code(4)
            rooms[room] = {'members': 0, "messages": {}}
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
    return render_template('room.html')

@socketio.on('connect')
def joined(auth):
    room = session.get('room')
    username = session.get('username')
    if not room or not username:
        return
    if room not in rooms:
        leave_room(room)
        return
    join_room(room)
    emit('status', {'msg': username + 'has entered the room.'}, room=room)
    rooms[room]['members'] += 1
    print(f'{username} joined room {room}')
    print(rooms)

@socketio.on('disconnect')
def left():
    room = session.get('room')
    username = session.get('username')
    leave_room(room)
    if room in rooms:
        rooms[room]['members'] -= 1
        if rooms[room]['members'] <= 0:
            del rooms[room]

    emit('status', {'msg': username + ' has left the room.'}, room=room)
    print(f'{username} has left the room')
    print(rooms)

@socketio.on('text', namespace='/chat')
def text(message):
    room = session.get('room')
    emit('message', {'msg': session.get('username') + ':' + message['msg']}, room=room)