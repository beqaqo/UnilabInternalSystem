from flask_restx import  reqparse, inputs, fields, Resource
from flask_jwt_extended import jwt_required, current_user

from app.extensions import api
from app.api.validators.authentication import check_validators

profile_ns = api.namespace('Profile', description='Api endpoint for User Profile related operations', path="/api")

profile_model = profile_ns.model('Profile', {
    'firstname': fields.String(required=True, description='First name',example='რომა'),
    'surname': fields.String(required=True, description='Last name',example='გრიგალაშვილი'),
    'email': fields.String(required=True, description='Email address',example='roma.grigalasvili@gmail.com'),
    'number': fields.String(required=True, description='Phone number',example='555222111'),
    'personal_id': fields.String(required=True, description='Personal ID',example='12234512891'),
    'date': fields.DateTime(required=True, description='Date of birth', dt_format='iso8601',example='2024-06-25T15:22:57.338Z'),
    'gender': fields.String(required=True, description='Gender',example='მამრობითი',enum =["მდედრობითი","მამრობითი",]),
    'password': fields.String(required=True, description='Password',example='password'),
    'password_new': fields.String(required=True, description='New password',example='password'),
    'region_id': fields.Integer(required=True, description='Region ID',example='1'),
    'city_id': fields.Integer(required=True, description='City ID',example='1'),
    'address': fields.String(required=True, description='Address',example='მისამართი..'),
    'role_id': fields.Integer(required=True, description='Role ID' , example = 2),
    'school': fields.String(required=True, description='School' ,example = '1 public high school'),
    'grade': fields.String(required=True, description='Grade' , example = "10"),
    'parent_name': fields.String(required=True, description='Parent\'s name', example = "Imeda"),
    'parent_lastname': fields.String(required=True, description='Parent\'s last name', example = "Grigalashvili"),
    'parent_number': fields.String(required=True, description='Parent\'s phone number', example = "566666555"),
    'university_id': fields.Integer(required=True, description='University ID', example = 1),
    'faculty': fields.String(required=True, description='Faculty', example = "Science"),
    'program': fields.String(required=True, description='Program', example = "Ml modeling"),
    'semester': fields.String(required=True, description='Semester', example = "Summer 2024"),
    'degree_level': fields.String(required=True, description='Degree level', example = "Masters"),
    'about_me': fields.String(required=True, description='Degree level', example = "Masters")
})

parser = reqparse.RequestParser()
parser.add_argument("firstname", required=True, type=str, help="Name example: Roma (1-50 characters)")
parser.add_argument("surname", required=True, type=str, help="Last name example: Grigalashhvili ")
parser.add_argument("email", required=True, type=str, help="Email example: example@gmail.com ")
parser.add_argument("number", required=True, type=str, help="Phone number example: 123456789")
parser.add_argument("personal_id", required=True, type=str, help="Personal ID example: 12345678901 (11 characters)")
parser.add_argument("date", required=True, type=inputs.datetime_from_iso8601, help="Date of birth example: 1999-10-27")
parser.add_argument("gender", required=True, type=str, help="Gender example: Male/Female")
parser.add_argument("password", required=True, type=str, help="Password example: password123 ")
parser.add_argument("password_new", required=True, type=str, help="New password (Should not match password)")
parser.add_argument("region_id", required=True, type=int, help="Region ID example: 11 (Cities and regions should be a match)")
parser.add_argument("city_id", required=True, type=int, help="City ID example: 2 (Cities and regions should be a match)")
parser.add_argument("address", required=True, type=str, help="Address example: 123 Main St")
parser.add_argument("role_id", required=True, type=int, help="Role ID example: 2  (1- is for admin)")
parser.add_argument("school", required=True, type=str, help="School example: High School")
parser.add_argument("grade", required=True, type=str, help="Grade example: 10th Grade ")
parser.add_argument("parent_name", required=True, type=str, help="Parent's name example: John ")
parser.add_argument("parent_lastname", required=True, type=str, help="Parent's last name example: Doe ")
parser.add_argument("parent_number", required=True, type=str, help="Parent's phone number example: 123456789 ")
parser.add_argument("university_id", required=True, type=int, help="University ID example: 1")
parser.add_argument("faculty", required=True, type=str, help="Faculty example: Engineering ")
parser.add_argument("program", required=True, type=str, help="Program example: Computer Science")
parser.add_argument("semester", required=True, type=str, help="Semester example: 1st Semester")
parser.add_argument("degree_level", required=True, type=str, help="Degree level example: Bachelor")
parser.add_argument("about_me", required=True, type=str, help="About me: I work in IT company")


@profile_ns.route('/profile')
@profile_ns.doc(responses={200: 'OK', 400: 'Invalid Argument'})
class UserProfileApi(Resource):

    @jwt_required()
    @profile_ns.doc(security='JsonWebToken')
    @profile_ns.marshal_with(profile_model)
    def get(self):
        if current_user:
            user_data = current_user.to_json()
            return user_data, 200

        return "User not found", 404

    @jwt_required()
    @profile_ns.doc(security='JsonWebToken')
    @profile_ns.doc(parser=parser)
    def put(self):

        args = parser.parse_args()
        validation = check_validators(parser, user_check=False, role_check = False, terms_check = False)

        if validation:
            return validation

        if current_user and current_user.check_password(args["password"]):

            current_user.name = args["name"]
            current_user.lastname = args["lastname"]
            current_user.email = args["email"]
            current_user.number = args["number"]
            current_user.personal_id = args["personal_id"]
            current_user.date = args["date"]
            current_user.gender = args["gender"]
            current_user.password = args["password_new"]
            current_user.country_id = args["country_id"]
            current_user.region_id = args["region_id"]
            current_user.city_id = args["city_id"]
            current_user.address = args["address"]
            current_user.school = args["school"]
            current_user.grade = args["grade"]
            current_user.parent_name = args["parent_name"]
            current_user.parent_lastname = args["parent_lastname"]
            current_user.parent_number = args["parent_number"]
            current_user.university_id = args["university_id"]
            current_user.faculty = args["faculty"]
            current_user.program = args["program"]
            current_user.semester = args["semester"]
            current_user.degree_level = args["degree_level"]
            current_user.about_me = args["about_me"]

            current_user.save()

            return "Successfully updated User's profile", 200

        return "Bad request", 400