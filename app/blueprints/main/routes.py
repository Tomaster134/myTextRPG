from flask import request, render_template, redirect, url_for, session, flash
from flask_login import login_required, current_user
from . import main

rooms = {}

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

@main.route('/room')
def room():
    if current_user.is_authenticated:
        location = session.get('location')
        print(f'room route is {location}')
        return render_template('room.html')
    else:
        flash('Login in first, bubs', 'warning')
        return redirect(url_for('auth.login'))