from flask_restx import Resource, reqparse
from flask_jwt_extended import jwt_required, current_user

from app.models import Certificate
from app.extensions import api

certificate_ns = api.namespace('Certificate', path='/api', description='Api endpoint for certificates related operations')

parser = reqparse.RequestParser()
parser.add_argument("user_id", required=True, type=str)
parser.add_argument("announcement_id", required=True, type=str)

@certificate_ns.route('/certificate')
class CertificateApi(Resource):

    @jwt_required()
    @certificate_ns.doc(security='JsonWebToken', parser=parser)
    def get(self):
        received_arguments = parser.parse_args()
        certificates = Certificate.query

        if received_arguments["user_id"] and current_user.is_admin:
            certificates = certificates.filter(Certificate.user_id == received_arguments["user_id"])
        else:
            certificates = certificates.filter(Certificate.user_id == current_user.id)

        certificates = certificates.all()

        if not certificates:
            return "You don't have any Certificates", 404

        certificates_data = [certificate.to_json() for certificate in certificates]

        return certificates_data, 200

    @jwt_required()
    @certificate_ns.doc(security='JsonWebToken', parser=parser)
    def post(self):
        request_parser = parser.parse_args()

        if not current_user.check_permission("can_create_certificates"):
            return "You can't create Certificates", 403

        new_certificate = Certificate(
            user_id=request_parser["user_id"],
            announcement_id=request_parser["announcement_id"],
        )

        new_certificate.create()
        new_certificate.save()

        return "Success", 200
