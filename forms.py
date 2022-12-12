from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, EmailField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class LoginForm(FlaskForm):
    email = EmailField("Email: ")
    psw = PasswordField("Password ", validators=[DataRequired(), Length(min=4, max=100)])
    remember = BooleanField("Remember", default=False)
    sub = SubmitField('Enter')


class RegistrForm(FlaskForm):
    username = StringField("Username: ")
    email = EmailField("Email: ")
    password = PasswordField("Password ", validators=[DataRequired(), Length(min=4, max=100)])
    psw1 = PasswordField("RePassword ", validators=[DataRequired(), EqualTo('password', message='Passwords do not match')])
    sub = SubmitField('Registration')