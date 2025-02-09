from app.extensions import api
from app.api.authentication import  AuthorizationApi, RegistrationApi, AccessTokenRefreshApi
from app.api.registration_activities import RegistrationActivitiesApi
from app.api.userprofile import UserProfileApi
from app.api.certificate import CertificateApi
from app.api.announcement import AnnouncementApi
from app.api.portfolio import PortfolioApi
from app.api.subjects import SubjectApi
from app.api.mail import ConfirmEmailApi, SendConfirmEmailApi
from app.api.lists import listApi