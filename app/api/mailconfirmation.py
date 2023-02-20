from flask_restful import Resource, reqparse
from flask import render_template
from app.models.user import User
from app.api.validators.mail import create_key, send_email,confirm_key



class SendConfirmEmailApi(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("email", required=True, type=str )

    def post(self):
        parser = self.parser.parse_args()
        user = User.query.filter_by(email = parser["email"]).first() 
        if user and not user.confirmed:
            key = create_key(parser["email"])
            html = render_template('_activation_massage.html', key=key)
            
            send_email(subject = "Confirm your account", html=html, recipients=parser["email"])
            return "Success", 200
        return "invalid mail"
    

    
class ReceiveConfirmEmailApi(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("key", required=True, type=str )

    def post(self):
        parser = self.parser.parse_args()
        email = confirm_key(parser["key"])
        user = User.query.filter_by(email=email).first()
        if user and not user.confirmed:
            user.confirmed = True
            user.save()
            return "Success"
        else:
            return "Wrong secret key or expired, or already confirmed"