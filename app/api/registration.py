from flask_restful import Resource, reqparse
from app.models.user import User


class RegistrationApi(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument("name", required=True, type=str )
    parser.add_argument("lastname", required=True, type=str)
    parser.add_argument("email", required=True, type=str)
    parser.add_argument("number", required=True, type=str)
    parser.add_argument("date", required=True, type=str )
    parser.add_argument("gender", required=True, type=str)


    parser.add_argument("password", required=True, type=str )
    parser.add_argument("password", required=True, type=str)



    parser.add_argument("country", required=True, type=str)
    parser.add_argument("region", required=True, type=str )
    parser.add_argument("city", required=True, type=str)
    parser.add_argument("address", required=True, type=str)

    parser.add_argument("role", required=True, type=str )

    parser.add_argument("school", required=True, type=str)
    parser.add_argument("grade", required=True, type=str)
    parser.add_argument("parent_name", required=True, type=str)
    parser.add_argument("parent_lastname", required=True, type=str)
    parser.add_argument("parent_number", required=True, type=str)


    parser.add_argument("university", required=True, type=str)
    parser.add_argument("faculty", required=True, type=str)
    parser.add_argument("program", required=True, type=str)
    parser.add_argument("semester", required=True, type=str)
    parser.add_argument("degree_level", required=True, type=str)


    parser.add_argument("terms", required=True, type=str)


    def post(self):
        new_parser = self.parser
        parser = new_parser.parse_args()
        new_user = User(username=parser["username"], email=parser["email"], password=parser["password"])

        new_user.create()
        new_user.save()

        return "Success", 200



    def get(self):

        return "Method Not Allowed", 405


    def put(self):

        return "Method Not Allowed", 405


    def delete(self):

        return "Method Not Allowed", 405