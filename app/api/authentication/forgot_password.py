from flask import render_template
from flask_jwt_extended import create_access_token
from flask_restx import reqparse, Resource
from datetime import timedelta

from app.api.authentication import auth_ns
from app.utils.mail import send_email
from app.models import User

parser = reqparse.RequestParser()
parser.add_argument("email", required=True, type=str)

@auth_ns.route('/forgot_password')
@auth_ns.doc(responses={200: 'OK', 400: 'Invalid Argument'})
class ForgotPasswordApi(Resource):
    @auth_ns.expect(parser)
    def post(self):
        args = parser.parse_args()

        user = User.query.filter_by(email=args["email"]).first()
        if not user:
            return "მომხმარებელი მითითებული მეილით არ არსებობს", 400

        reset_token = create_access_token(identity=user.email, expires_delta=timedelta(minutes=5))
        html = render_template('_reset_password_email.html', token=reset_token)
        send_email(subject="პაროლის აღდგენა", html=html, recipients=args["email"])

        return f"/reset_password/{reset_token}", 200 # TODO: Remove reset token once we move to production