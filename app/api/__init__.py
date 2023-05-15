from flask import Blueprint
from flask_restful import Api
from .users import UserResource, UsersResource
from .post import PostsResource, PostResource, PostsUserResource, LikeResource, DislikeResource, LikesResource, \
    DislikesResource
from .auth import GenerateTokenResource
from .profile import ProfileResource

bp = Blueprint('api', __name__, url_prefix='/api')
api = Api(bp)

api.add_resource(UsersResource, '/users', endpoint="users_list")
api.add_resource(UserResource, '/users/<int:user_id>', endpoint="users_details")
api.add_resource(UserResource, '/users/<string:username>', endpoint="users_details_username")

api.add_resource(PostsResource, '/posts', endpoint="posts_list")
api.add_resource(PostsUserResource, '/posts/user/<int:autor_id>', endpoint="users_posts_list")
api.add_resource(PostResource, '/posts/<int:id>', endpoint="posts_list_by_id")

api.add_resource(LikeResource, '/post/<int:post_id>/like/<int:user_id>', endpoint="like_post_by_id")
api.add_resource(LikesResource, '/likes', endpoint="all_likes")
api.add_resource(LikeResource, '/like/<int:id>', endpoint="special_like_id")

api.add_resource(DislikeResource, '/post/<int:post_id>/dislike/<int:user_id>', endpoint="dislike_post_by_id")
api.add_resource(DislikesResource, '/dislikes', endpoint="all_dislikes")
api.add_resource(DislikeResource, '/dislike/<int:id>', endpoint="special_dislike_id")

api.add_resource(ProfileResource, '/profile/<int:user_id>', endpoint="profile_by_user_id")

api.add_resource(GenerateTokenResource, '/generate_token', endpoint="generate_token")
