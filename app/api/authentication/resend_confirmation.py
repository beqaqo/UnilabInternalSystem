from flask import render_template
from flask_jwt_extended import jwt_required
from flask_restx import reqparse, Resource

from app.api.authentication import auth_ns
from app.utils.mail import create_key, send_email
from app.models import User

parser = reqparse.RequestParser()
parser.add_argument("email", required=True, type=str)

@auth_ns.route('/resend_confirmation')
class ResendConfirmEmailApi(Resource):
    @jwt_required()
    @auth_ns.doc(security='JsonWebToken', parser=parser)
    def post(self):
        args = parser.parse_args()
        user = User.query.filter_by(email=args["email"]).first()
        if user and not user.confirmed:
            key = create_key(args["email"])
            html = render_template('_activation_massage.html', key=key)

            send_email(subject="მომხმარებლის გააქტიურება", html=html, recipients=args["email"])
            return f"/confirm_user/{key}", 200
        return 400