from flask_jwt_extended import current_user, jwt_required
from flask_restx import reqparse, Resource

from app.api.announcements import announcement_ns
from app.models import Announcement, AnnouncementForm

parser = reqparse.RequestParser()
parser.add_argument("announcement_id", required=True, type=int)
parser.add_argument("form_id", required=True, type=int)


@announcement_ns.route('/announcement_form')
class AnnouncementFormApi(Resource):
    @jwt_required()
    @announcement_ns.doc(security='JsonWebToken')
    def get(self):
        if not current_user.check_permission("can_create_activity"):
            return "თქვენ არ შეგიძლიათ აქტივობის ფორმების ნახვა", 403

        announcements = Announcement.get_all_announcements()

        return announcements, 200

    @jwt_required()
    @announcement_ns.doc(security='JsonWebToken')
    @announcement_ns.doc(parser=parser)
    def post(self):
        request_parser = self.parser.parse_args()

        if not current_user.check_permission("can_create_activity"): #TODO: Add permission for this
            return "თქვენ არ შეგიძლიათ აქტივობაზე ფორმების მიბმა", 403

        new_announcement_form = AnnouncementForm(
            announcement_id=request_parser["announcement_id"],
            form_id=request_parser["form_id"],
        )
        new_announcement_form.create()
        new_announcement_form.save()

        return 200