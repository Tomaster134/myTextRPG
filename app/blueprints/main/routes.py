from flask import request, render_template, redirect, url_for, session, flash
from flask_login import login_required, current_user
from ... import socketio
from flask_socketio import join_room, leave_room, emit
from . import main
import app.blueprints.main.events as events

@main.route('/', methods=['POST', 'GET'])
def index():
        if request.method == 'POST':
            if current_user.is_authenticated:
                location = current_user.location
                username = current_user.username
                
                session['location'] = location
                session["username"] = username
                return redirect(url_for('main.room'))
            else: 
                flash('Login in first, bubs', 'warning')
                return redirect(url_for('auth.login'))

        else: return render_template('index.html')

def world_timer():
     socketio.sleep(10)
     count = 0
     while True:
            if events.client_list:
                print('world timer')
                socketio.emit('look', {'message': f'this is a global emitter on count {count}'})
                count += 1
                socketio.sleep(10)
            else: break

@main.route('/room')
def room():
    print(f'session for app is {session}')
    if not events.client_list:
        socketio.start_background_task(world_timer)
    if current_user.is_authenticated:
        location = session.get('location')
        print(f'room route is {location}')
        return render_template('room.html')
    else:
        flash('Login in first, bubs', 'warning')
        return redirect(url_for('auth.login'))