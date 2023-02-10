from flask_restful import Resource, reqparse
from app.models.user import User
from app.api.validators.registation import *



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


        if not name_validator(parser["name"]):
            return "Invalid name", 400

        if not name_validator(parser["lastname"]):
            return "Invalid lastname", 400

        if not mail_validator(parser["email"]):
            return "Invalid email",   400

        if not number_validator(parser["number"]):
            return "Invalid number",   400     

        if not id_validator(parser["personal_ID"]):
            return "Invalid personal_ID", 400

        if parser["role"] == "მოსწავლე" and not name_validator(parser["parent_name"]):
            return "Invalid parent_name", 400

        if parser["role"] == "მოსწავლე" and not name_validator(parser["parent_lastname"]):
            return "Invalid parent_lastname", 400

        if parser["role"] == "მოსწავლე" and not number_validator(parser["parent_number"]):
            return "Invalid parent_number", 400


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
                            parent_number = str(parser["parent_number"]),
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

