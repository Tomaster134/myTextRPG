from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class RoomForm(FlaskForm):
    username = StringField('Username: ', validators=[DataRequired()])
    join_btn = SubmitField('Join')