from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length
import logging
"""
LoginForm and RegisterForm

"""

class LoginForm(FlaskForm):
   # def __init__(self):
        #logging.INFO #* read about logging in Python

    username = StringField("Username", validators=[DataRequired(), Length(min=4, max=50)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=4, max=50)])


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=4, max=50)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=4, max=50)])

# Abstract class, parent class and inherit 2 child class.

