from flask import request, render_template, redirect, url_for, session, flash
from flask_login import login_required, current_user
from ... import socketio
from flask_socketio import join_room, leave_room, emit
from . import main
import app.blueprints.main.events as events
from random import randint

#First page user sees. Should be a blurb on the game, and direct users towards either logging in, signing up, creating a character, or changing their active character
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

#Function that runs when there are players in the world. Uses sleep and will eventually call all objects that need to execute methods without user input for world ambience. When no players are present should break and stop the function
def world_timer():
     socketio.sleep(10)
     count = 0
     while True:
            if events.client_list:
                socketio.emit('event', {'message': f'this is a global emitter on count {count}'})
                count += 1
                socketio.sleep(10)
            else: break

#Route for the room. Calls the world timer function if the client list is empty to begin a world timer.
@main.route('/room')
def room():
    print(f'session for app is {session}')
    if not events.client_list:
        socketio.start_background_task(world_timer)
    if current_user.is_authenticated:
        if current_user.active_account:
            return render_template('room.html')
        else:
             flash('Please create a player before joining the world.', 'warning')
             return redirect(url_for('auth.create'))
    else:
        flash('Login in first, bubs', 'warning')
        return redirect(url_for('auth.login'))