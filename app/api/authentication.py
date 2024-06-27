from flask_restx import Resource
from flask import render_template
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity


from app.models import User, Country, UserRole, Role
from app.api.validators import check_validators,create_key, send_email
from app.extensions import api
from app.api.nsmodels import reg_ns, registration_model, reg_parser, auth_parser





@reg_ns.route('/registration')
@reg_ns.doc(responses={200: 'OK', 400: 'Invalid Argument'})
class RegistrationApi(Resource):
    @reg_ns.doc(parser=reg_parser)
    def post(self):
        args = reg_parser.parse_args()
        validation = check_validators(args)
        if validation:
            return validation

        new_user = User(
            name=args["name"],
            lastname=args["lastname"],
            email=args["email"],
            password=args["password"],
            personal_id=args["personal_id"],
            number=args["number"],
            date=args["date"],
            gender=args["gender"],
            country_id=args["country_id"],
            region_id=args["region_id"],
            city_id=args["city_id"],
            address=args["address"],
            school=args["school"],
            grade=args["grade"],
            parent_name=args["parent_name"],
            parent_lastname=args["parent_lastname"],
            parent_number=args["parent_number"],
            university_id=args["university_id"],
            faculty=args["faculty"],
            program=args["program"],
            semester=args["semester"],
            degree_level=args["degree_level"]
        )

        new_user.create()
        new_user.save()

        new_user_role = UserRole(user_id=new_user.id, role_id=args["role_id"])
        new_user_role.create()
        new_user_role.save()

        key = create_key(args["email"])
        html = render_template('_activation_massage.html', key=key)
        send_email(subject="Confirm your account", html=html, recipients=args["email"])

        return "Successfully registered a User", 200
  
    def get(self):
        locations = Country.get_locations()
        roles = Role.get_roles()

        data = {
            "locations": locations,
            "roles": roles
        }

        return data, 200

@reg_ns.route('/login')
@reg_ns.doc(responses={200: 'OK', 400: 'Invalid Argument'})
class AuthorizationApi(Resource):
    @reg_ns.doc(parser=auth_parser)
    def post(self):
        args = auth_parser.parse_args()

        user = User.query.filter_by(email=args["email"]).first()
        if not user:
            return "User with this email does not exist", 400

        if user.check_password(args["password"]):
            access_token = create_access_token(identity=user)
            refresh_token = create_refresh_token(identity=user)
            response = {
                "access_token": access_token,
                "refresh_token": refresh_token
            }
            return response
        else:
            return "Password is incorrect", 400

@reg_ns.route('/refresh')

class AccessTokenRefreshApi(Resource):
    @jwt_required()
    @reg_ns.doc(security='JsonWebToken')
    def post(self):
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity)
        response = {
            "access_token": access_token
        }

        return response
