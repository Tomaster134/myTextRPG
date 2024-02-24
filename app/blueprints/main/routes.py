from flask import request, render_template, redirect, url_for, session
from . import main
from ... import socketio
from flask_socketio import join_room, leave_room, send, emit
import random
from string import ascii_uppercase

@main.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')