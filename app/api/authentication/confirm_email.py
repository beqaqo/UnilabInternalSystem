from flask_restx import Resource
from flask_jwt_extended import jwt_required

from app.api.authentication import auth_ns
from app.utils.mail import confirm_key
from app.models import User

@auth_ns.route('/confirm_email/<token>')
class ConfirmEmailApi(Resource):
    def post(self, token):
        email = confirm_key(token)

        user = User.query.filter_by(email=email).first()
        if user and not user.confirmed:
            user.confirmed = True
            user.save()

            return "Successfully confimed user", 200
        else:
            return "Wrong secret key or expired, or already confirmed", 400