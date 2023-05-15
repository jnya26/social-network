from marshmallow import EXCLUDE
from marshmallow.fields import Nested
from marshmallow_sqlalchemy import SQLAlchemyAutoSchemaOpts, SQLAlchemyAutoSchema

from app import db
from app.models import User, Profile, Posts, Like


class BaseOpts(SQLAlchemyAutoSchemaOpts):
    """
    Base schema configurations:
        * session
        * unknown
        """


def __init__(self, meta, ordered=False):
    if not hasattr(meta, "sqla_session"):
        meta.sqla_session = db.session
    if not hasattr(meta, "unknown"):
        meta.unknown = EXCLUDE
    if not hasattr(meta, "load_instance"):
        meta.load_instance = True
    if not hasattr(meta, "include_fk"):
        meta.include_fk = True
    super(BaseOpts, self).__init__(meta, ordered=ordered)


class BaseSchema(SQLAlchemyAutoSchema):
    """
    Base configured schema class
    """
    OPTIONS_CLASS = BaseOpts


class ProfileSchema(BaseSchema):
    class Meta:
        model = Profile
        fields = ('user_id', 'first_name', 'last_name', 'bio', 'last_seen', 'linkidln_link', 'facebook_link',
                  'country', 'photo')


class PostSchema(BaseSchema):
    class Meta:
        model = Posts
        fields = ('autor_id', 'title', 'content', 'likes', 'dislikes', 'created_at', 'id', 'photo',)


class LikeSchema(BaseSchema):
    class Meta:
        model = Like
        fields = ('id', 'created_at', 'post_id', 'user_id',)


class UserSchema(BaseSchema):
    class Meta:
        model = User
        exclude = ('password',)
        # fields = ('id',) - choose any exactly field.
        # exclude = ('password') - exclude from all functions, where is use this scheme.

    # profile - relation name in models.User
    profile = Nested(ProfileSchema(), many=False)
