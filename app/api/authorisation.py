from flask_restful import Resource, reqparse
from app.models.user import User




class AuthorizationApi(Resource):

    parser = reqparse.RequestParser()

    parser.add_argument("email", required=True, type=str )
    parser.add_argument("password", required=True, type=str)



    def post(self):

        parser = self.parser.parse_args()

        user = User.query.filter_by(email = parser["email"]).first()
    

        if bool(user) and user.check_password(parser["password"]):           
            return "Success", 200

        else:
            return "Password or mail is incorrect", 400