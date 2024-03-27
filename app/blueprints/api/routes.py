from . import api
from flask import request, jsonify, session
from app.models import User, PlayerAccount
from werkzeug.security import check_password_hash
from sqlalchemy import exc

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
            'user_active_account': current_user.active_account,            
        })
    else:
        return jsonify({
            'status': 'login error',
            'message': 'username or password did not match',
        })
    
@api.post('/signup')
def signup_api():
    '''
    payload should include:
    {
    "username": string,
    "email": string,
    "password": string,
    }
    '''

    data = request.get_json()
    username = data['username']
    email = data['email']
    password = data['password']
    try:
        new_user = User(username, email, password)
        new_user.save()
        return jsonify({
                'status': 'ok',
                'message': 'signup successful',
                })
    except exc.IntegrityError:
        return jsonify({
            'status': 'error',
            'message': 'username or email taken',
        })

@api.post('/user_pull')
def user_pull_api():
    '''
    payload should include:
    {
    user_id: number,
    }'''

    data = request.get_json()
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
            'message': 'could not find user',
        })
    
@api.post('/create')
def create_api():
    '''
    payload should include:
    {
    user_id: number,
    player_name: string,
    }
    '''
    data = request.get_json()
    user_id = data['user_id']
    player_name = data['player_name']
    current_user = User.query.filter(User.id == user_id).first()
    first_account = False
    if current_user.accounts.all() == []:
        first_account = True
    if not first_account:
        for account in current_user.accounts.all():
            account.is_active = False
            account.save()
    try:
        new_player = PlayerAccount(user_id=current_user.id, player_name=player_name, is_active=True)
        new_player.save()
        current_user.active_account = new_player.id
        current_user.save()
        return jsonify({
            'status': 'ok',
            'message': 'player account created',
        })
    except exc.IntegrityError:
        return jsonify({
            'status': 'error',
            'message': 'player name already in use',
        })
    

@api.get('/player_accounts')
def player_accounts_api():
    '''
    query should include:
    {
    user_id: number,
    }
    '''
    print(request.args)
    user_id = request.args['user_id']
    current_user = User.query.filter(User.id == user_id).first()
    accounts = current_user.accounts.all()
    payload = {}
    for account in accounts:
        entry = {
            'player_name': account.player_name,
            'is_active': account.is_active,
            'player_id': account.id,
        }
        payload.update({account.id: entry})
    return jsonify({
        'status': 'ok',
        'accounts': payload,
    })

@api.post('/change_active')
def change_active_api():
    '''
    payload should include:
    {
    user_id: number,
    player_id: number,
    }
    '''
    data = request.get_json()
    user_id = data['user_id']
    new_active = data['player_id']
    current_user = User.query.filter(User.id == user_id).first()
    for account in current_user.accounts.all():
            account.is_active = False
            account.save()
    player = PlayerAccount.query.filter(PlayerAccount.id == new_active).first()
    player.is_active = True
    player.save()
    return jsonify({
        'status': 'ok',
        'new_active': player.id,
        'active_name': player.player_name,
    })