from flask_wtf import FlaskForm
from wtforms import StringField, validators


class LoginForm(FlaskForm):
    login = StringField('login', [validators.DataRequired()])
    password = StringField('password', [validators.DataRequired()])
