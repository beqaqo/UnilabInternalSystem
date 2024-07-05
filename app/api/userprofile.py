from flask_restx import Resource
from app.api.validators.authentication import check_validators
from flask_jwt_extended import jwt_required, current_user

from app.extensions import api
from app.api.nsmodels import profile_ns, profile_model, profile_parser


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
    @profile_ns.doc(parser=profile_parser)
    def put(self):

        parser = profile_parser.parse_args()
        validation = check_validators(parser, user_check=False, role_check = False, terms_check = False)

        if validation:
            return validation

        if current_user and current_user.check_password(parser["password"]):

            current_user.name = parser["name"]
            current_user.lastname = parser["lastname"]
            current_user.email = parser["email"]
            current_user.number = parser["number"]
            current_user.personal_id = parser["personal_id"]
            current_user.date = parser["date"]
            current_user.gender = parser["gender"]
            current_user.password = parser["password_new"]
            current_user.country_id = parser["country_id"]
            current_user.region_id = parser["region_id"]
            current_user.city_id = parser["city_id"]
            current_user.address = parser["address"]
            current_user.school = parser["school"]
            current_user.grade = parser["grade"]
            current_user.parent_name = parser["parent_name"]
            current_user.parent_lastname = parser["parent_lastname"]
            current_user.parent_number = parser["parent_number"]
            current_user.university_id = parser["university_id"]
            current_user.faculty = parser["faculty"]
            current_user.program = parser["program"]
            current_user.semester = parser["semester"]
            current_user.degree_level = parser["degree_level"]
            current_user.about_me = parser["about_me"]

            current_user.save()

            return "Successfully updated User's profile", 200

        return "Bad request", 400
