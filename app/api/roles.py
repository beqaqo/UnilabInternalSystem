from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User
from app.models.roles import UserRole


class CreateRoles(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument("user_id", required=True, type=int)
    parser.add_argument("role_id", required=True, type=int)

    @jwt_required()
    def post(self):
        parser = self.parser.parse_args()
        current_user = get_jwt_identity()
        user = User.query.filter_by(email=current_user).first()

        if user.check_permission("can_create_roles"):
            user_role = UserRole(
                user_id=parser["user_id"], role_id=parser["role_id"])
            user_role.create()
            user_role.save()
            return "Success", 200
        return "Bad request", 400

    @jwt_required()
    def put(self):
        parser.add_argument("new_role_id", required=True, type=int)

        parser = self.parser.parse_args()
        current_user = get_jwt_identity()
        user = User.query.filter_by(email=current_user).first()

        if user.check_permission("can_create_roles"):

            result = UserRole.query.filter(
                user_id=parser["user_id"], role_id=parser["role_id"]).first()
            if result:
                result.role_id = parser["new_role_id"]
                result.save()
                return "Success", 200
            return "Bad request", 400

        return "Bad request", 400

    @jwt_required()
    def delete(self):
        parser = self.parser.parse_args()
        current_user = get_jwt_identity()
        user = User.query.filter_by(email=current_user).first()

        if user.check_permission("can_create_roles"):

            result = UserRole.query.filter(
                user_id=parser["user_id"], role_id=parser["role_id"]).first()
            if result:
                result.delete()
                result.save()
                return "Success", 200
            return "Bad request", 400

        return "Bad request", 400
