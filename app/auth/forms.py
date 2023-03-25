from flask_wtf import FlaskForm
from wtforms import (
StringField,
PasswordField,
BooleanField,
SubmitField,
validators,
EmailField
)

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[validators.DataRequired()])
    password = PasswordField("Password", validators=[validators.DataRequired()])
    remmember = BooleanField("Remmember")
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[validators.DataRequired()])
    password = PasswordField("Password", validators=[validators.DataRequired()])
    email = EmailField("Email", validators=[validators.DataRequired()])
    submit = SubmitField("Login")