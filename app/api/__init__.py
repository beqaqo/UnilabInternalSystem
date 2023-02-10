from flask_restful import Api
from app.api.registration import RegistrationApi


api = Api()
api.add_resource(RegistrationApi, "/Registration")