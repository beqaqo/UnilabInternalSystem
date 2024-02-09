from flask_restful import Api
from app.api.authentication import RegistrationApi, AuthorizationApi, AccessTokenRefreshApi
from app.api.mailconfirmation import SendConfirmEmailApi, ReceiveConfirmEmailApi
from app.api.registration_activities import RegistrationActivitiesApi
from app.api.userprofile import UserProfileApi
from app.api.roles import RolesApi
from app.api.announcement import AnnouncementApi, AnnouncementFormApi
from app.api.questions import QuestionApi, QuestionFormApi, FormApi, UserAnswerApi
from app.api.certificate import CertificateApi
from app.api.subjects import SubjectApi

api = Api()
api.add_resource(RegistrationApi, "/registration")
api.add_resource(AuthorizationApi, "/authorization")
api.add_resource(AccessTokenRefreshApi, "/refresh_access_token")
api.add_resource(SendConfirmEmailApi, "/send_confirm_email")
api.add_resource(ReceiveConfirmEmailApi, "/receive_confirm_email")
api.add_resource(UserProfileApi, "/user_profile")
api.add_resource(RolesApi, "/roles")
api.add_resource(AnnouncementApi, "/announcement", "/announcement/<int:id>")
api.add_resource(AnnouncementFormApi, "/announcement_form")
api.add_resource(QuestionApi, "/question")
api.add_resource(QuestionFormApi, "/question_form")
api.add_resource(RegistrationActivitiesApi, "/registration_activities")
api.add_resource(FormApi, "/form")
api.add_resource(UserAnswerApi, "/user_answer")
api.add_resource(CertificateApi, "/certificate")
api.add_resource(SubjectApi, "/subject")
