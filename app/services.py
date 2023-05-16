from app import db
from app.models import User, Profile, Posts, Like, Dislike
from schemas import UserSchema, PostSchema, ProfileSchema


class UserService:
    def get_by_id(self, user_id):
        user = db.session.query(User).filter(User.id == user_id).first_or_404()
        return user

    def get_by_username(self, username):
        user = db.session.query(User).filter(User.username == username).first_or_404()
        return user

    def create(self, **kwargs):
        user = User(username=kwargs.get('username'), email=kwargs.get('email'))
        user.set_password(kwargs.get('password'))
        db.session.add(user)
        db.session.commit()

        profile = Profile(first_name="To be update", last_name="To be update",
                          linkidln_link="To be update", facebook_link="To be update", instagram_link="To be update",
                          twitter_link="To be update",
                          user_id=user.id, country="No info",
                          photo="https://img.freepik.com/free-icon/user_318-875902.jpg")
        db.session.add(profile)
        db.session.commit()
        return user

    def update(self, data):
        user = UserSchema(exclude=("password",)).load(data)
        return user

    def delete(self, user_id):
        user = self.get_by_id(user_id)
        profile = user.profile
        db.session.delete(profile)
        db.session.commit()

        db.session.delete(user)
        db.session.commit()
        return True


class ProfileService:
    def get_by_id(self, user_id):
        profile = db.session.query(Profile).filter(Profile.user_id == user_id).first()
        return profile

    def update(self, data):
        profile = ProfileSchema().load(data)
        return profile


class PostService:
    def get_by_id(self, id):
        post = db.session.query(Posts).filter(Posts.id == id).first_or_404()
        return post

    def get_by_autor(self, autor_id):
        post = db.session.query(Posts).filter(Posts.autor_id == autor_id).all()
        return post

    def create(self, **kwargs):
        post = Posts(title=kwargs.get('title'), content=kwargs.get('content'), autor_id=kwargs.get('autor_id'))
        db.session.add(post)
        db.session.commit()
        return post

    def update(self, data):
        post = PostSchema(exclude=('autor_id',)).load(data)
        return post


class LikeService:
    def get_like_by_post_id(self, post_id):
        like = db.session.query(Like).filter(Like.post_id == post_id).count()
        return like

    def get_like_by_like_id(self, id):
        like = db.session.query(Like).filter(Like.id == id).first()
        return like

    def create(self, user_id, post_id):
        like_post = Like(user_id=user_id, post_id=post_id)
        db.session.add(like_post)
        db.session.commit()

    def delete_like(self, user_id, post_id):
        like = db.session.query(Like).filter(Like.post_id == post_id, Like.user_id == user_id).first()
        return like


class DislikeService:
    def get_dislike_by_post_id(self, post_id):
        dislike = db.session.query(Dislike).filter(Dislike.post_id == post_id).count()
        return dislike

    def get_like_by_dislike_id(self, id):
        dislike = db.session.query(Dislike).filter(Dislike.id == id).first()
        return dislike

    def create(self, user_id, post_id):
        dislike_post = Dislike(user_id=user_id, post_id=post_id)
        db.session.add(dislike_post)
        db.session.commit()

    def delete_dislike(self, user_id, post_id):
        dislike = db.session.query(Dislike).filter(Dislike.post_id == post_id, Dislike.user_id == user_id).first()
        return dislike
