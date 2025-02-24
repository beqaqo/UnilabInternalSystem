from flask_jwt_extended import create_access_token, create_refresh_token
from flask_restx import reqparse, Resource

from app.models import User
from app.api.authentication import auth_ns


parser = reqparse.RequestParser()
parser.add_argument("email", required=True, type=str)
parser.add_argument("password", required=True, type=str)

@auth_ns.route('/login')
@auth_ns.doc(responses={200: 'OK', 400: 'Invalid Argument'})
class LoginApi(Resource):
    @auth_ns.doc(parser=parser)
    def post(self):
        args = parser.parse_args()

        user = User.query.filter_by(email=args["email"]).first()
        if not user:
            return "მომხმარებელი მითითებული მეილით არ არსებობს", 400

        if user.check_password(args["password"]):
            access_token = create_access_token(identity=user)
            refresh_token = create_refresh_token(identity=user)
            response = {
                "access_token": access_token,
                "refresh_token": refresh_token
            }
            return response
        else:
            return "პაროლი არ არის სწორი", 400