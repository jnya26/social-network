from datetime import datetime
from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)


class User(BaseModel, UserMixin):
    username = db.Column(db.String, unique=True, index=True)
    email = db.Column(db.String, unique=True, index=True)
    password = db.Column(db.String, nullable=False)

    posts = db.relationship(
        "Posts", backref="author", uselist=True, lazy="dynamic", cascade="all,delete"
    )
    likes = db.relationship(
        'Like', backref='user', lazy='dynamic', primaryjoin='User.id==Like.user_id', cascade="all,delete"
    )
    dislikes = db.relationship(
        'Dislike', backref='user', lazy='dynamic', primaryjoin='User.id==Dislike.user_id', cascade="all,delete"
    )
    # list of users that follow you
    follower = db.relationship("Follow", backref="follower", foreign_keys="Follow.follower_id")

    # list of users that you follow
    following = db.relationship("Follow", backref="followee", foreign_keys="Follow.followee_id")

    activities = db.relationship("Activities", backref='autor', uselist=True, lazy="dynamic", cascade="all,delete")

    def is_follow(self, user):
        if db.session.query(Follow).filter(Follow.follower_id == self.id, Follow.followee_id == user.id).first():
            print(self.id)
            return True

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f"{self.username}({self.email})"


class Profile(BaseModel):
    __tablename__ = "profiles"
    __table_args__ = (
        db.Index("idx_profiles_user_id", "user_id"),
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id", name="fk_profiles_user_id", ondelete="CASCADE"),
        nullable=False
    )
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    bio = db.Column(db.String)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    linkidln_link = db.Column(db.String)
    facebook_link = db.Column(db.String)
    twitter_link = db.Column(db.String)
    instagram_link = db.Column(db.String)
    country = db.Column(db.String)
    photo = db.Column(db.String)

    user = db.relationship("User", backref=db.backref("profile", uselist=False), uselist=False)


class Posts(BaseModel):
    __tablename__ = "posts"
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    autor_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id", name="fk_post_autor_id", ondelete="CASCADE"),
        nullable=False)

    likes = db.relationship("Like", backref="post", uselist=True, cascade="all,delete")
    dislikes = db.relationship("Dislike", backref="post", uselist=True, cascade="all,delete")


class Activities(BaseModel):
    __tablename__ = "activities"
    action = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    autor_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id", name="fk_post_autor_id", ondelete="CASCADE"),
        nullable=False)


class Like(BaseModel):
    __tablename__ = "likes"
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id", name="fk_likes_user_id"),
        nullable=False)
    post_id = db.Column(
        db.Integer,
        db.ForeignKey("posts.id", name="fk_likes_post_id"),
        nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Dislike(BaseModel):
    __tablename__ = "dislikes"
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id", name="fk_dislikes_user_id"),
        nullable=False)
    post_id = db.Column(
        db.Integer,
        db.ForeignKey("posts.id", name="fk_dislikes_post_id"),
        nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Follow(db.Model):
    __tablename__ = "followers"

    follower_id = db.Column(db.Integer, db.ForeignKey("user.id", name="fk_follows_follower_id"), primary_key=True)
    followee_id = db.Column(db.Integer, db.ForeignKey("user.id", name="fk_follows_followee_id"), primary_key=True)
