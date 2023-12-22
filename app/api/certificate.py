from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, current_user
from app.models import Certificate


class CertificateApi(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument("user_id", required=True, type=str)
    parser.add_argument("announcement_id", required=True, type=str)

    @jwt_required()
    def get(self):

        get_parser = reqparse.RequestParser()
        get_parser.add_argument("user_id", type=int, required=False, location="args")

        received_arguments = get_parser.parse_args()
        certificates = Certificate.query

        if received_arguments["user_id"] and current_user.is_admin:
            certificates = certificates.filter(Certificate.user_id == received_arguments["user_id"])
        else:
            certificates = certificates.filter(Certificate.user_id == current_user.id)

        certificates = certificates.all()

        if not certificates:
            return "You don't have any certificates", 200

        certificates_data = [certificate.to_json() for certificate in certificates]

        return certificates_data, 200

    @jwt_required()
    def post(self):
        request_parser = self.parser.parse_args()

        if not current_user.check_permission("can_create_certificates"):
            return "Bad request", 400

        new_certificate = Certificate(
            user_id=request_parser["user_id"],
            announcement_id=request_parser["announcement_id"],
        )

        new_certificate.create()
        new_certificate.save()

        return "Success", 200
