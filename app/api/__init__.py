from flask_restful import Api
from app.api.authentication import RegistrationApi, AuthorizationApi
from app.api.mailconfirmation import SendConfirmEmailApi, ReceiveConfirmEmailApi
from app.api.registration_activities import RegistrationActivitiesApi
from app.api.userprofile import UserProfileApi
from app.api.roles import RolesApi
from app.api.announcement import AnnouncementApi, AnnouncementFormApi
from app.api.questions import QuestionApi, FormApi, UserAnswerApi
from app.api.certificate import CertificateApi

api = Api()
api.add_resource(RegistrationApi, "/Registration")
api.add_resource(AuthorizationApi, "/Authorization")
api.add_resource(SendConfirmEmailApi, "/SendConfirmEmail")
api.add_resource(ReceiveConfirmEmailApi, "/ReceiveConfirmEmail")
api.add_resource(UserProfileApi, "/UserProfile")
api.add_resource(RolesApi, "/Roles")
api.add_resource(AnnouncementApi, "/Announcement", "/announcement/<int:id>")
api.add_resource(AnnouncementFormApi, "/AnnouncementForm")
api.add_resource(QuestionApi, "/Question")
api.add_resource(RegistrationActivitiesApi, '/registration_activities')
api.add_resource(FormApi, '/Form')
api.add_resource(UserAnswerApi, "/send_answers")
api.add_resource(CertificateApi, "/certificate")
