from flask_restx import Resource
from flask_jwt_extended import jwt_required, current_user
from app.models import User, Announcement, AnnouncementForm, AnnouncementLecturer
from app.api.nsmodels import announcement_parser, announcement_ns, announcement_form_parser, announcement_model



@announcement_ns.route('/announcement')
@announcement_ns.doc(responses={200: 'OK', 400: 'Invalid Argument'})
class AnnouncementApi(Resource):
    @jwt_required()
    @announcement_ns.doc(security='JsonWebToken')
    @announcement_ns.expect(announcement_model)
    def post(self):
        args = announcement_parser.parse_args()

        if not current_user.check_permission("can_create_activity"):
            return "You can't create Announcements", 403

        new_announcement = Announcement(
            name=args["name"],
            subject_id=args["subject_id"],
            activity_type_id=args["activity_type_id"],
            registration_start=args["registration_start"],
            registration_end=args["registration_end"],
            start_date=args["start_date"],
            end_date=args["end_date"]
        )
        new_announcement.create()
        new_announcement.save()

        lecturer_ids = args["lecturer_ids"]
        for lecturer_id in lecturer_ids:
            lecturer = User.query.filter_by(id=lecturer_id).first()
            if not lecturer:
                print(f"User with ID {lecturer_id} does not exist")
                return f"User with ID {lecturer_id} does not exist", 400

            # print(f"Checking roles for User ID {lecturer_id}")
            # print(f"User roles: {[role.name for role in lecturer.role]}")

            if not lecturer.has_role("ლექტორი"):
                print(f"User with ID {lecturer_id} is not a lecturer")
                return f"User with ID {lecturer_id} is not a lecturer", 400

            announcement_user = AnnouncementLecturer(
                user_id=lecturer_id,
                announcement_id=new_announcement.id
            )
            announcement_user.create()
            announcement_user.save()

        return "Successfully created an Announcement", 200





@announcement_ns.route('/announcement/<int:id>')
@announcement_ns.doc(responses={200: 'OK', 400: 'Invalid Argument'})
class AnnouncementApi(Resource):
    @jwt_required()
    @announcement_ns.doc(security = 'JsonWebToken')
    @announcement_ns.expect( announcement_model)
    def put(self, id):

        if not current_user.check_permission("can_create_activity"):
            return "You can't create Announcements", 403
        
        args = announcement_parser.parse_args()
       
        result = Announcement.query.get(id)
      

        if not result:
            return "Announcement not found", 404

        result.name = args["name"]
        result.subject_id = args ["subject_id"]
        result.activity_type_id = args["activity_type_id"]
        result.registration_start = args["registration_start"]
        result.registration_end = args["registration_end"]
        result.start_date = args["start_date"]
        result.end_date = args["end_date"]

        result.save()     

        lecturer_ids = args["lecturer_ids"]
        for lecturer_id in lecturer_ids:
            lecturer = User.query.filter_by(id=lecturer_id).first()
            if not lecturer:
                print(f"User with ID {lecturer_id} does not exist")
                return f"User with ID {lecturer_id} does not exist", 400

            # print(f"Checking roles for User ID {lecturer_id}")
            # print(f"User roles: {[role.name for role in lecturer.role]}")

            if not lecturer.has_role("ლექტორი"):
                print(f"User with ID {lecturer_id} is not a lecturer")
                return f"User with ID {lecturer_id} is not a lecturer", 400

            announcement_user = AnnouncementLecturer(
                user_id=lecturer_id,
                announcement_id=result.id
            )
            announcement_user.create()
            announcement_user.save()

        return "Successfully updated an Announcement", 200
    @jwt_required()
    @announcement_ns.doc(security = 'JsonWebToken')
    
    def delete(self, id):

        result = Announcement.query.get(id) 

        if not current_user.check_permission("can_create_activity"):
            return "You can't create or delete Announcements", 403
         
        if not result:
            return "Announcement not found", 404
        
        

        result.delete()
        result.save()

        return "Successfully deleted an Announcement", 200


@announcement_ns.route('/announcement_form')
class AnnouncementFormApi(Resource):
    @jwt_required()
    @announcement_ns.doc(security = 'JsonWebToken')
    def get(self):
        if not current_user.check_permission("can_create_activity"):
            return "You can't create Announcement Forms", 403

        announcements = Announcement.get_all_announcements()

        return announcements, 200
    
    @jwt_required()
    @announcement_ns.doc(security = 'JsonWebToken')
    @announcement_ns.doc(parser = announcement_form_parser)
    def post(self):
        request_parser = self.parser.parse_args()

        if not current_user.check_permission("can_create_activity"):
            return "You can't create Announcement forms", 403

        new_announcement_form = AnnouncementForm(
            announcement_id=request_parser["announcement_id"],
            form_id=request_parser["form_id"],
        )
        new_announcement_form.create()
        new_announcement_form.save()

        return "Successfully created an Announcement form", 200