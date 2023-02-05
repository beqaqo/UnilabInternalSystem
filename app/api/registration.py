from flask_restful import Resource, reqparse
from app.models.user import User


class RegistrationApi(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument("username", required=True, type=str )
    parser.add_argument("email", required=True, type=str)
    parser.add_argument("password", required=True, type=str)



    def post(self):
        new_parser = self.parser
        parser = new_parser.parse_args()
        new_user = User(username=parser["username"], email=parser["email"], password=parser["password"])

        new_user.create()
        new_user.save()

        return "Success", 200

