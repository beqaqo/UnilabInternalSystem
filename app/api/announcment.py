from flask_restful import Resource, reqparse, inputs
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User
from app.models.subjects import Announcement


class CreateAnnouncment(Resource):
    

    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        user = User.query.filter_by(email=current_user).first()

        if user.check_permission("can_create_roles"):
            data = Announcement.query.all()
            return data, 200
        return "Bad request", 400

    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name", required=True, type=str)
        parser.add_argument("subject_id", required=True, type=int)
        parser.add_argument("activity_type_id", required=True, type=int)
        parser.add_argument("lecturer_id", required=True, type=int)
        parser.add_argument("regitration_start", required=True,
                            type=inputs.datetime_from_iso8601)
        parser.add_argument("regitration_end", required=True,
                            type=inputs.datetime_from_iso8601)

        request_parser = parser.parse_args()
        current_user = get_jwt_identity()
        user = User.query.filter_by(email=current_user).first()

        if user.check_permission("can_create_activity"):
            new_anouncement = Announcement(
                name=request_parser["name"],
                subject_id=request_parser["subject_id"],
                activity_type_id=request_parser["activity_type_id"],
                lecturer_id=request_parser["lecturer_id"],
                regitration_start=request_parser["regitration_start"],
                regitration_end=request_parser["regitration_end"],
            )
            new_anouncement.create()
            new_anouncement.save()
            return "Success", 200
        return "Bad request", 400

    @jwt_required()
    def put(self):
        parser.add_argument("announcment_id", required=True, type=int)
        parser.add_argument("name", required=True, type=str)
        parser.add_argument("subject_id", required=True, type=int)
        parser.add_argument("activity_type_id", required=True, type=int)
        parser.add_argument("lecturer_id", required=True, type=int)
        parser.add_argument("regitration_start",
                            required=True, type=inputs.datetime_from_iso8601)
        parser.add_argument("regitration_end",
                            required=True, type=inputs.datetime_from_iso8601)

        parser = self.parser.parse_args()
        current_user = get_jwt_identity()
        user = User.query.filter_by(email=current_user).first()

        if user.check_permission("can_create_activity"):
            result = Announcement.query.filter(id=parser["announcment_id"]).first()
            if result:
                result.name = parser["name"]
                result.ubject_id = parser["subject_id"]
                result.activity_type_id = parser["activity_type_id"]
                result.lecturer_id = parser["lecturer_id"]
                result.regitration_start = parser["regitration_start"]
                result.regitration_end = parser["regitration_end"]
                result.save()
                return "Success", 200
            return "Bad request", 400

    @jwt_required()
    def delete(self):
        parser.add_argument("announcment_id", required=True, type=int)
        parser = self.parser.parse_args()
        current_user = get_jwt_identity()
        user = User.query.filter_by(email=current_user).first()

        if user.check_permission("can_create_activity"):
            result = Announcement.query.filter(
                id=parser["announcment_id"]).first()
            if result:
                result.delete()
                result.save()
                return "Success", 200
            return "Bad request", 400

        return "Bad request", 400
