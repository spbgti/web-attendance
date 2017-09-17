from flask_wtf import FlaskForm, validators
from wtforms import StringField


class LoginForm(FlaskForm):
    login = StringField('login', [validators])
    password = StringField('password', [validators])

#delete