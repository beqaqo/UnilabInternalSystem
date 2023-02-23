from flask_restful import Api
from app.api.authentication import RegistrationApi, AuthorizationApi
from app.api.mailconfirmation import SendConfirmEmailApi, ReceiveConfirmEmailApi


api = Api()
api.add_resource(RegistrationApi, "/Registration")
api.add_resource(AuthorizationApi, "/Authorization")
api.add_resource(SendConfirmEmailApi, "/SendConfirmEmail")
api.add_resource(ReceiveConfirmEmailApi, "/ReceiveConfirmEmail")


