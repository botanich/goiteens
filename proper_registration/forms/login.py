from flask_wtf import FlaskForm
from wtforms import validators, StringField, PasswordField, SubmitField


class LoginForm(FlaskForm):
    nickname = StringField('Nickname', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])
    submit = SubmitField("Log in")
