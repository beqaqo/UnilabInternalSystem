from flask_restful import Api
from app.api.authentication import RegistrationApi, AuthorizationApi


api = Api()
api.add_resource(RegistrationApi, "/Registration")
api.add_resource(AuthorizationApi, "/Authorization")