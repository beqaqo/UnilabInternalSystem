from flask_restful import Resource, reqparse
from flask import render_template
from app.models.user import User
from app.api.validators.mail import create_key, send_email, confirm_key

from flask_jwt_extended import jwt_required

class SendConfirmEmailApi(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("email", required=True, type=str)

    @jwt_required()
    def post(self):
        parser = self.parser.parse_args()
        user = User.query.filter_by(email=parser["email"]).first()
        if user and not user.confirmed:
            key = create_key(parser["email"])
            html = render_template('_activation_massage.html', key=key)

            send_email(subject="Confirm your account", html=html, recipients=parser["email"])
            
            return "Successfully sent mail confirmation", 200
        
        return "No email was sent or it was invaild", 400


class ReceiveConfirmEmailApi(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("key", required=True, type=str)

    @jwt_required()
    def post(self):
        parser = self.parser.parse_args()
        email = confirm_key(parser["key"])

        user = User.query.filter_by(email=email).first()
        if user and not user.confirmed:
            user.confirmed = True
            user.save()

            return "Successfully confimed user", 200
        else:
            return "Wrong secret key or expired, or already confirmed", 400
