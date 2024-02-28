from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

#Extraneous, need to make sure removal is OK, but no reason to have a username and join form when login is required.
class RoomForm(FlaskForm):
    username = StringField('Username: ', validators=[DataRequired()])
    join_btn = SubmitField('Join')