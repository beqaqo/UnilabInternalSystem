from app.api.authentication.confirm_email import ConfirmEmailApi
from app.api.authentication.forgot_password import ForgotPasswordApi
from app.api.authentication.login import LoginApi
from app.api.authentication.refresh import AccessTokenRefreshApi
from app.api.authentication.register import RegistrationApi
from app.api.authentication.reset_password import ResetPasswordApi
from app.api.authentication.resend_confirmation import ResendConfirmEmailApi


from app.api.lists.locations import LocationApi
from app.api.lists.roles import RoleApi
from app.api.lists.schools import SchoolApi
from app.api.lists.universities import UniversityApi

from app.api.announcements.announcement import AnnouncementApi
from app.api.announcements.announcement_form import AnnouncementFormApi

from app.api.profile import UserProfileApi
from app.api.certificate import CertificateApi
from app.api.portfolio import PortfolioApi
from app.api.subject import SubjectApi