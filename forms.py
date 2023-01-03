from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import InputRequired


class AddUserForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
