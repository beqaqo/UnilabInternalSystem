from flask_jwt_extended import get_jwt_identity
from flask_restx import Resource, reqparse

from app.api.authentication import auth_ns
from app.models import User


parser = reqparse.RequestParser()
parser.add_argument("token", required=True, type=str)
parser.add_argument("new_password", required=True, type=str)

@auth_ns.route('/reset_password')
@auth_ns.doc(responses={200: 'OK', 400: 'Invalid Argument'})
class ResetPasswordApi(Resource):
    @auth_ns.expect(parser)
    def post(self):
        args = parser.parse_args()
        new_password = args.get("new_password")

        try:
            email = get_jwt_identity()
        except Exception:
            return "ტოკენი არ არის სწორი ან გაუვიდა ვადა", 400

        user = User.query.filter_by(email=email).first()
        if not user:
            return "მომხმარებელი ვერ მოიძებნა", 400

        user.set_password(new_password)
        user.save()

        return 200