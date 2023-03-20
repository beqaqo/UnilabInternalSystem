from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User
from app.models.roles import UserRole


class CreateRoles(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument("user_mail", required=True, type=str)
    parser.add_argument("role_id", required=True, type=int)

    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        user = User.query.filter_by(email=current_user).first()

        if not user.check_permission("can_create_roles"):
            return "Bad request", 400

        roles = [{"user_mail": User.query.filter_by(id=object.user_id).first().email, 
                  "role_id": object.role_id} for object in UserRole.query.all()]

        return roles, 200

    @jwt_required()
    def post(self):
        parser = self.parser.parse_args()
        current_user = get_jwt_identity()
        user = User.query.filter_by(email=current_user).first()

        if not user.check_permission("can_create_roles"):
            return "Bad request", 400

        user_role = UserRole(user_id=User.query.filter_by(
            email=parser["user_mail"]).first().id, role_id=parser["role_id"])

        user_role.create()
        user_role.save()
        return "Success", 200

    @jwt_required()
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument("user_mail", required=True, type=str)
        parser.add_argument("role_id", required=True, type=int)
        parser.add_argument("new_role_id", required=True, type=int)

        parser = parser.parse_args()
        current_user = get_jwt_identity()
        user = User.query.filter_by(email=current_user).first()

        if not user.check_permission("can_create_roles"):
            return "Bad request", 400

        result = UserRole.query.filter_by(user_id=User.query.filter_by(
            email=parser["user_mail"]).first().id, role_id=parser["role_id"]).first()

        if not result:
            return "Bad request", 400

        result.role_id = parser["new_role_id"]
        result.save()
        return "Success", 200

    @jwt_required()
    def delete(self):
        parser = self.parser.parse_args()
        current_user = get_jwt_identity()
        user = User.query.filter_by(email=current_user).first()

        if not user.check_permission("can_create_roles"):
            return "Bad request", 400

        result = UserRole.query.filter_by(user_id=User.query.filter_by(
            email=parser["user_mail"]).first().id, role_id=parser["role_id"]).first()

        if not result:
            return "Bad request", 400

        result.delete()
        result.save()
        return "Success", 200
