from flask_restful import Resource, reqparse
from app.models.user import User
from app.api.validators.registation import check_validators



class RegistrationApi(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument("name", required=True, type=str )
    parser.add_argument("lastname", required=True, type=str)
    parser.add_argument("email", required=True, type=str)
    parser.add_argument("number", required=True, type=int)
    parser.add_argument("personal_ID", required=True, type=int)
    parser.add_argument("date", required=True, type=str)
    parser.add_argument("gender", required=True, type=str)
   

    parser.add_argument("password", required=True, type=str )
    parser.add_argument("conf_password", required=True, type=str)

    parser.add_argument("country", required=True, type=str)
    parser.add_argument("region", required=True, type=str )
    parser.add_argument("city", required=True, type=str)
    parser.add_argument("address", required=True, type=str)

    parser.add_argument("role", required=True, type=str )

    parser.add_argument("school", required=True, type=int)
    parser.add_argument("grade", required=True, type=int)
    parser.add_argument("parent_name", required=True, type=str)
    parser.add_argument("parent_lastname", required=True, type=str)
    parser.add_argument("parent_number", required=True, type=int)

    parser.add_argument("university", required=True, type=str)
    parser.add_argument("faculty", required=True, type=str)
    parser.add_argument("program", required=True, type=str)
    parser.add_argument("semester", required=True, type=int)
    parser.add_argument("degree_level", required=True, type=str)

    parser.add_argument("terms", required=True, type=bool)



    


    def post(self):
        
        parser = self.parser.parse_args()


        if check_validators(parser):
            return check_validators(parser)




        if bool(User.query.filter_by(email = parser["email"]).first()):
            return "This mail is already redgistered", 400

        if bool(User.query.filter_by(number = parser["number"]).first()):
            return "This number is already redgistered", 400

        if bool(User.query.filter_by(personal_ID = parser["personal_ID"]).first()):
            return "This personal_ID is already redgistered", 400
        


        if parser["password"] == parser["conf_password"] and parser["terms"] :

            new_user = User(name=parser["name"], 
                            lastname = parser["lastname"], 
                            email = parser["email"],
                            password = parser["password"],
                            personal_ID = str(parser["personal_ID"]),
                            number = str(parser["number"]),
                            date = parser["date"],
                            gender = parser["gender"],
                            country = parser["country"],
                            region = parser["region"],
                            city = parser["city"],
                            address = parser["address"],
                            role = parser["role"],
                            school = parser["school"],
                            grade = parser["grade"],
                            parent_name = parser["parent_name"],
                            parent_lastname = parser["parent_lastname"],
                            parent_number = str(parser["parent_number"] ),          # str გამომიგზავნის ფრონტი?
                            university = parser["university"],
                            faculty = parser["faculty"],
                            program = parser["program"],
                            semester = parser["semester"],
                            degree_level = parser["degree_level"]
                            )


            new_user.create()
            new_user.save()

            return "Success", 200
        
        else:

            return "Invalid request", 400

