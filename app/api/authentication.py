from flask_restful import Resource, reqparse, inputs
from app.models.user import User
from app.api.validators.authentication import check_validators



class RegistrationApi(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument("name", required=True, type=str )
    parser.add_argument("lastname", required=True, type=str)
    parser.add_argument("email", required=True, type=str)
    parser.add_argument("number", required=True, type=str)
    parser.add_argument("personal_id", required=True, type=str)
    parser.add_argument("date", required=True, type=inputs.datetime_from_iso8601)
    parser.add_argument("gender", required=True, type=str)
   
    parser.add_argument("password", required=True, type=str )
    parser.add_argument("conf_password", required=True, type=str)

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

    parser.add_argument("terms", required=True, type=bool)

    
    


    def post(self):
        
        parser = self.parser.parse_args()
        validation = check_validators(parser, User)



        if validation:
            return validation
        

        new_user = User(
                        name=parser["name"], 
                        lastname = parser["lastname"], 
                        email = parser["email"],
                        password = parser["password"],
                        personal_id = parser["personal_id"],
                        number = parser["number"],
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
                        parent_number = parser["parent_number"],  
                        university = parser["university"],
                        faculty = parser["faculty"],
                        program = parser["program"],
                        semester = parser["semester"],
                        degree_level = parser["degree_level"]
        
                    
                        )


        new_user.create()
        new_user.save()





        return "Success", 200




class AuthorizationApi(Resource):

    parser = reqparse.RequestParser()

    parser.add_argument("email", required=True, type=str )
    parser.add_argument("password", required=True, type=str)



    def post(self):

        parser = self.parser.parse_args()

        user = User.query.filter_by(email = parser["email"]).first()
    

        if user and user.check_password(parser["password"]):           
            return "Success", 200
        else:
            return "Password or mail is incorrect", 400
        












    




