from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, validators


class CreatPost(FlaskForm):
    title = StringField('Title', validators=[validators.data_required(message="Invalid data"),
                                             validators.Length(min=2, max=100)])
    content = TextAreaField("Content", validators=[validators.data_required(message="Invalid data"),
                                                   validators.Length(min=10, max=5000)])

    submit = SubmitField('Post')
