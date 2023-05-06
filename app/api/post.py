from flask_restful import Resource
from flask import jsonify, request
from app import db
from app.models import Posts
from app.services import PostService, LikeService, DislikeService
from schemas import PostSchema, LikeSchema

post_service = PostService()

like_service = LikeService()
dislike_service = DislikeService()


class PostsResource(Resource):
    def get(self):
        ordered = request.args.get('ordered', type=bool)
        posts_query = db.session.query(Posts)
        if ordered:
            posts_query = posts_query.ordered_by(Posts.created_at.asc())
        posts = posts_query.all()
        return jsonify(PostSchema().dump(posts, many=True))

    def post(self):
        json_data = request.get_json()
        post = post_service.create(**json_data)

        response = jsonify(PostSchema().dump(post, many=False))
        response.status_code = 201
        return response


class PostsUserResource(Resource):
    def get(self, autor_id):
        post = post_service.get_by_autor(autor_id)
        return jsonify(PostSchema().dump(post, many=True))


class PostResource(Resource):
    def get(self, id):
        post = post_service.get_by_id(id)
        post_data = PostSchema().dump(post, many=False)
        post_data['likes'] = like_service.get_like_by_post_id(id)
        post_data['dislikes'] = dislike_service.get_dislike_by_post_id(id)
        return jsonify(post_data)

    def put(self, id):
        json_data = request.get_json()
        json_data['id'] = id
        post = post_service.update(json_data)
        return jsonify(PostSchema().dump(post, many=False))

    def delete(self, id):
        post = post_service.get_by_id(id)
        db.session.delete(post)
        db.session.commit()
        return True


class LikeResource(Resource):
    def post(self, user_id, post_id):
        like = like_service.create(user_id, post_id)
        response = jsonify(LikeSchema().dump(like, many=False))
        response.status_code = 201
        return True

    def delete(self, user_id, post_id):
        like = like_service.delete_like(user_id, post_id)
        db.session.delete(like)
        db.session.commit()
        return True


class DislikeResource(Resource):
    def post(self, user_id, post_id):
        dislike = dislike_service.create(user_id, post_id)
        response = jsonify(LikeSchema().dump(dislike, many=False))
        response.status_code = 201
        return True

    def delete(self, user_id, post_id):
        dislike = dislike_service.delete_dislike(user_id, post_id)
        db.session.delete(dislike)
        db.session.commit()
        return True
