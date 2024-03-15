from . import api
from flask import request, jsonify, session
from app.models import User, PlayerAccount
from werkzeug.security import check_password_hash

@api.post('/login')
def login_api():
    '''
    payload should include:
    {
    "username": string,
    "password": string,
    }
    '''

    data = request.get_json()
    username = data['username']
    password = data['password']
    queried_user = User.query.filter(User.username == username).first()
    if queried_user and check_password_hash(queried_user.password, password):
        current_user = queried_user
        return jsonify({
            'status': 'logged in',
            'user_id': current_user.id,
            'user_email': current_user.email,
            'user_username': current_user.username,
            'user_active_account': current_user.active_account            
        })
    else:
        return jsonify({
            'status': 'login error',
            'message': 'username or password did not match'
        })

@api.post('/user_pull')
def user_pull_api():
    '''
    payload should include:
    {
    user_id: number
    }'''

    data = request.get_json()
    print(session)
    user_id = data['user_id']
    queried_user = User.query.filter(User.id == user_id).first()
    if queried_user:
        current_user = queried_user
        return jsonify({
            'status': 'ok',
            'user_id': current_user.id,
            'user_email': current_user.email,
            'user_username': current_user.username,
            'user_active_account': current_user.active_account            
        })
    else:
        return jsonify({
            'status': 'error',
            'message': 'could not find user'
        })