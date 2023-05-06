from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField, validators, BooleanField
from wtforms.validators import Length


class ProfileForm(FlaskForm):
    country = StringField('Country')
    first_name = StringField("First Name")
    last_name = StringField("Last Name")
    bio = TextAreaField('About me', validators=[Length(min=0, max=360)])
    facebook_link = StringField('Facebook')
    linkidln_link = StringField('LinkedIn')
    confirm_update = BooleanField("Confirm Updates", validators=[validators.DataRequired()])
    submit = SubmitField('Submit')


class EditPasswordForm(FlaskForm):
    password = PasswordField(validators=[
        validators.DataRequired(message="Password is required"),
        validators.Length(min=6, message="Min 6 length of password is required")])
    confirm_password = PasswordField("Confirm Password", validators=[
        validators.DataRequired(message="Password is required"),
        validators.Length(min=6, message="Min 6 length of password is required"),
        validators.EqualTo('password', message='Passwords must match')])
