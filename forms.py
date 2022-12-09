from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, EmailField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, Length

class LoginForm(FlaskForm):
    email = EmailField("Email: ")
    psw = PasswordField("Password ", validators=[DataRequired(), Length(min=4, max=100)])
    remember = BooleanField("Remember", default=False)
    sub = SubmitField('Enter')
