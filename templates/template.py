from flask_wtf import FlaskForm
from wtforms import IntegerField, PasswordField, validators


class LoginForm(FlaskForm):
    login = IntegerField('login', [validators.DataRequired()])
    password = PasswordField('password', [validators.DataRequired()])
