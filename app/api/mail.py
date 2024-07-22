from flask_restx import Resource, reqparse
from flask import render_template
from app.models.user import User
from app.api.validators.mail import create_key, send_email, confirm_key
from app.api.nsmodels.mail import mail_ns, parser

from flask_jwt_extended import jwt_required


@mail_ns.route('/resend_confirmation')
class SendConfirmEmailApi(Resource):
    @jwt_required()
    @mail_ns.doc(security='JsonWebToken', parser=parser)
    def post(self):
        args = parser.parse_args()
        user = User.query.filter_by(email=args["email"]).first()
        if user and not user.confirmed:
            key = create_key(args["email"])
            html = render_template('_activation_massage.html', key=key)

            send_email(subject="Confirm your account", html=html, recipients=args["email"])
            
            return "Successfully sent mail confirmation", 200
        
        return "No email was sent or it was invaild", 400


@mail_ns.route('/confirm_email/<token>')
class ConfirmEmailApi(Resource):
    @jwt_required()
    @mail_ns.doc(security='JsonWebToken')
    def post(self, token):
        email = confirm_key(token)

        user = User.query.filter_by(email=email).first()
        if user and not user.confirmed:
            user.confirmed = True
            user.save()

            return "Successfully confimed user", 200
        else:
            return "Wrong secret key or expired, or already confirmed", 400
