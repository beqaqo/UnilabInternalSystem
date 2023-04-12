from flask_restful import Api
from app.api.authentication import RegistrationApi, AuthorizationApi
from app.api.mailconfirmation import SendConfirmEmailApi, ReceiveConfirmEmailApi
from app.api.userprofile import UserProfileApi
from app.api.roles import CreateRoles
from app.api.announcment import CreateAnnouncment
from app.api.questions import CreateQuestion

api = Api()
api.add_resource(RegistrationApi, "/Registration")
api.add_resource(AuthorizationApi, "/Authorization")
api.add_resource(SendConfirmEmailApi, "/SendConfirmEmail")
api.add_resource(ReceiveConfirmEmailApi, "/ReceiveConfirmEmail")
api.add_resource(UserProfileApi, "/UserProfile")
api.add_resource(CreateRoles, "/CreateRoles")
api.add_resource(CreateAnnouncment, "/CreateAnnouncment")
api.add_resource(CreateQuestion, "/CreateQuestion")