from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import InputRequired, Length, Optional


class SignupForm(FlaskForm):
    full_name = StringField("Full Name", validators=[InputRequired()])
    email = EmailField("Email", validators=[InputRequired()])
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[
                             InputRequired(), Length(min=8, max=20, message=None)])


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])


class BathroomForm(FlaskForm):
    name = StringField("Location Name", validators=[InputRequired()])
    address = StringField("Address", validators=[InputRequired()])
    zip_code = StringField("Zip Code", validators=[InputRequired()])
    website = StringField("Website", validators=[Optional()])
