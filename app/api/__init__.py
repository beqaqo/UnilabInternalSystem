from flask_restful import Api
from app.api.registration import RegistrationApi
from app.api.authorisation import AuthorizationApi

api = Api()
api.add_resource(RegistrationApi, "/Registration")
api.add_resource(AuthorizationApi, "/Authorization")