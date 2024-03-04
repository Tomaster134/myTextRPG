from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, PasswordField
from wtforms.validators import DataRequired

#Basic forms for signing in and logging in. Will be used to prevent users from reaching the room using Flask's Login Required decorated, and associating the current_user.id with the currently active player. Users should be able to have multiple players, but only one active player. Additionally, if player dies, a deceased tag will be added that prevents users from using that player 

class LoginForm(FlaskForm):
    username = StringField('Username: ', validators=[DataRequired()])
    password = PasswordField('Password: ', validators=[DataRequired()])
    login_btn = SubmitField('Login!')

class SignUpForm(FlaskForm):
    username = StringField('Username: ', validators=[DataRequired()])
    email = EmailField('Email: ', validators=[DataRequired()])
    password = PasswordField('Password: ', validators=[DataRequired()])
    signup_btn = SubmitField('Sign Up!')

class AccountForm(FlaskForm):
    player = StringField('Player Name:', validators=[DataRequired()])
    create_btn = SubmitField('Create a player!')