from flask import request, render_template, redirect, url_for, flash
from . import auth
from .forms import LoginForm, SignUpForm, AccountForm
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User, PlayerAccount
from werkzeug.security import check_password_hash
from sqlalchemy import exc

#Login route that checks the information from the login form against the database. If everything matches up, great, let 'em in. Uses WTFlask to prevent CSRF attacks
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit:
        username = form.username.data
        password = form.password.data

        queried_user = User.query.filter(User.username == username).first()
        if queried_user and check_password_hash(queried_user.password, password):
            flash(f'Login successful! Welcome back {queried_user.username}. Your current location is {queried_user.location}', 'info')
            login_user(queried_user)
            return redirect(url_for('main.index'))
        else:
            flash('Username or password incorrect :(', 'warning')
            return render_template('login.html', form=form)
    else:
        return render_template('login.html', form=form)

#Signup form that checks to see if the email or username is taken. If not, signs up user and enters their information into the database. Uses WTFlask to prevent CSRF attacks.
@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if request.method == 'POST' and form.validate_on_submit:
        username = form.username.data
        email = form.email.data
        password = form.password.data
        try:
            new_user = User(username, email, password)
            new_user.save()
            return redirect(url_for('auth.login'))
        except exc.IntegrityError:
            flash(f'Username or email already taken.', 'warning')
            return render_template('signup.html', form=form)
    else:
        return render_template('signup.html', form=form)

#Page to create an active account. Checks to see if this is the first player created, if not, sets all other players under that account to inactive and makes the newly created account active.
@auth.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = AccountForm()
    first_account = False
    if current_user.accounts.all() == []:
        first_account = True
    if request.method == 'POST' and form.validate_on_submit:
        player = form.player.data
        if not first_account:
            for account in current_user.accounts.all():
                account.is_active = False
                account.save()
        try:
            new_player = PlayerAccount(user_id=current_user.id, player_name=player, is_active=True)
            new_player.save()
            current_user.active_account = new_player.id
            current_user.save()
            flash(f'Player {player} has been created and set as active account!', 'success')
            return redirect(url_for('main.index'))
        except exc.IntegrityError:
            flash(f'Player name {player} already taken', 'warning')
            return render_template('create.html', form=form)
    else:
        return render_template('create.html', form=form)

#Logout route. Pretty straightforward.
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))