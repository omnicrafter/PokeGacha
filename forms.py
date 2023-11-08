from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, Length


class UserForm(FlaskForm):
    """Form for creating a user"""

    username = StringField('Username', validators=[
                           DataRequired(), Length(max=16)])
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=6)])
    email = StringField('Email', validators=[DataRequired(), Email()])


class UserLoginForm(FlaskForm):
    """Form for logging in user"""
    username = StringField('Username', validators=[
                           DataRequired(), Length(max=16)])
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=6)])


class UserEditForm(FlaskForm):
    """Form for editing a user"""


class PokemonEditForm(FlaskForm):
    """Form for editing a Pokemon"""
