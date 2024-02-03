from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, current_user
from app.models.user import User
from app.models.roles import UserRole

from app.extensions import db


class RolesApi(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument("user_email", required=True, type=str)
    parser.add_argument("role_id", required=True, type=int)
    parser.add_argument("new_role_id", required=False, type=int)

    @jwt_required()
    def get(self):
        if not current_user.check_permission("can_create_roles"):
            return "You can't create roles", 403
        
        users = User.query.options(db.joinedload(User.role)).all()

        users_with_roles = [
            {
                "user_email": user.email,
                "role_ids": [role.id for role in user.role]
            } for user in users
        ]
    
        return users_with_roles, 200

    @jwt_required()
    def post(self):
        parser = self.parser.parse_args()

        if not current_user.check_permission("can_create_roles"):
            return "You can't create roles", 403

        user_role = UserRole(user_id=User.query.filter_by(
            email=parser["user_email"]).first().id, role_id=parser["role_id"])

        user_role.create()
        user_role.save()

        return "Successfully created a Role for a user", 200

    @jwt_required()
    def put(self):
        parser = reqparse.RequestParser()

        parser = parser.parse_args()

        if not current_user.check_permission("can_create_roles"):
            return "You can't create or edit the roles", 403

        result = UserRole.query.filter_by(user_id=User.query.filter_by(
            email=parser["user_mail"]).first().id, role_id=parser["role_id"]).first()

        if not result:
            return "Role not found", 404

        result.role_id = parser["new_role_id"]
        result.save()

        return "Successfully creted a Role", 200

    @jwt_required()
    def delete(self):
        parser = self.parser.parse_args()

        if not current_user.check_permission("can_create_roles"):
            return "You can't create or delete the roles", 403

        result = UserRole.query.filter_by(user_id=User.query.filter_by(
            email=parser["user_mail"]).first().id, role_id=parser["role_id"]).first()

        if not result:
            return "Role not found", 404

        result.delete()
        result.save()

        return "Successfully deleted the Role", 200
