from flask_restful import Resource
from flask import jsonify, request
from app.services import ProfileService
from schemas import ProfileSchema

profile_service = ProfileService()


class ProfileResource(Resource):
    def get(self, user_id):
        profile = profile_service.get_by_id(user_id)
        return jsonify(ProfileSchema().dump(profile, many=False))

    def put(self, user_id):
        json_data = request.get_json()
        json_data['user_id'] = user_id

        profile = profile_service.update(json_data)
        return jsonify(ProfileSchema().dump(profile, many=False))
