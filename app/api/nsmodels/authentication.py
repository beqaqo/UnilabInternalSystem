from flask_restx import  reqparse, inputs, fields
from app.extensions import api


reg_ns = api.namespace('Authentification', description='ავთენთიპიკაციასთან დაკავშირებული ოპერაციები',path = '/api')




registration_model = reg_ns.model('Registration', {
    'name': fields.String(required=True, description='First name',example='გიორგი'),
    'lastname': fields.String(required=True, description='Last name',example='გვარაძე'),
    'email': fields.String(required=True, description='Email address',example='giorgi.gvaradze@gmail.com'),
    'number': fields.String(required=True, description='Phone number',example='5987654321'),
    'personal_id': fields.String(required=True, description='Personal ID',example='01234567891'),
    'date': fields.DateTime(required=True, description='Date of birth', dt_format='iso8601',example='2024-06-25T15:22:57.338Z'),
    'gender': fields.String(required=True, description='Gender',example='მამრობითი',enum =["მდედრობითი","მამრობითი",]),
    'password': fields.String(required=True, description='Password',example='password'),
    'conf_password': fields.String(required=True, description='Confirm password',example='password'),
    'region_id': fields.Integer(required=True, description='Region ID',example='1'),
    'city_id': fields.Integer(required=True, description='City ID',example='1'),
    'address': fields.String(required=True, description='Address',example='მისამართი..'),
    'role_id': fields.Integer(required=True, description='Role ID' , example = 2),
    'school': fields.String(required=True, description='School' ,example = '1 საჯარო სკოლა'),
    'grade': fields.String(required=True, description='Grade' , example = "10"),
    'parent_name': fields.String(required=True, description='Parent\'s name', example = "დავითი"),
    'parent_lastname': fields.String(required=True, description='Parent\'s last name', example = "გვარაძე"),
    'parent_number': fields.String(required=True, description='Parent\'s phone number', example = "599243115"),
    'university_id': fields.Integer(required=True, description='University ID', example = 1),
    'faculty': fields.String(required=True, description='Faculty', example = "კომპიუტერული მეცნიერება"),
    'program': fields.String(required=True, description='Program', example = "Ml modeling"),
    'semester': fields.String(required=True, description='Semester', example = "ზაფხული 2024"),
    'degree_level': fields.String(required=True, description='Degree level', example = "მაგისტრი"),
    'terms': fields.Boolean(required=True, description='Terms and conditions acceptance'),
})



# i think Parser is also applicable here

reg_parser = reqparse.RequestParser()

reg_parser.add_argument("name", required=True, type=str, help="Name example: Gorgi (1-50 characters)", location ='json')
reg_parser.add_argument("lastname", required=True, type=str, help="Last name example: Saldadze ", location ='json')
reg_parser.add_argument("email", required=True, type=str, help="Email example: example@example.com ", location ='json')
reg_parser.add_argument("number", required=True, type=str, help="Phone number example: 123456789", location ='json')
reg_parser.add_argument("personal_id", required=True, type=str, help="Personal ID example: 12345678901 (11 characters)", location ='json')
reg_parser.add_argument("date", required=True, type=inputs.datetime_from_iso8601, help="Date of birth example: YYYY-MM-DD", location ='json')
reg_parser.add_argument("gender", required=True, type=str, help="Gender example: Male/Female", location ='json')

reg_parser.add_argument("password", required=True, type=str, help="Password example: password", location ='json')
reg_parser.add_argument("conf_password", required=True, type=str, help="Confirm password (should match password)", location ='json')

reg_parser.add_argument("region_id", required=True, type=int, help="Region ID example: 11 (cities and regions should be a match)", location ='json')
reg_parser.add_argument("city_id", required=True, type=int, help="City ID example: 2 (cities and regions should be a match)", location ='json')
reg_parser.add_argument("address", required=True, type=str, help="Address example: 123 Main St", location ='json')

reg_parser.add_argument("role_id", required=True, type=int, help="Role ID example: 2  (1- is for admin)", location ='json')

reg_parser.add_argument("school", required=True, type=str, help="School example: High School", location ='json')
reg_parser.add_argument("grade", required=True, type=str, help="Grade example: 10th Grade ", location ='json')
reg_parser.add_argument("parent_name", required=True, type=str, help="Parent's name example: John ", location ='json')
reg_parser.add_argument("parent_lastname", required=True, type=str, help="Parent's last name example: Doe ", location ='json')
reg_parser.add_argument("parent_number", required=True, type=str, help="Parent's phone number example: 123456789 ", location ='json')

reg_parser.add_argument("university_id", required=True, type=int, help="University ID example: 1", location ='json')
reg_parser.add_argument("faculty", required=True, type=str, help="Faculty example: Engineering ", location ='json')
reg_parser.add_argument("program", required=True, type=str, help="Program example: Computer Science", location ='json')
reg_parser.add_argument("semester", required=True, type=str, help="Semester example: 1st Semester ", location ='json')
reg_parser.add_argument("degree_level", required=True, type=str, help="Degree level example: Bachelor", location ='json')
# reg_parser.add_argument('about me', required = True, type = str, help = 'my hobbies, etc '  )

reg_parser.add_argument("terms", required=True, type=bool, help="Terms and conditions acceptance example: true/false", location ='json')



# auth parser
auth_parser = reqparse.RequestParser()
auth_parser.add_argument("email", required=True, type=str)
auth_parser.add_argument("password", required=True, type=str)

# email parser
email_parser = reqparse.RequestParser()
email_parser.add_argument("email", required=True, type=str)


# password parser
password_parser = reqparse.RequestParser()
password_parser.add_argument("token", required=True, type=str)
password_parser.add_argument("new_password", required=True, type=str)
password_parser.add_argument("repeat_password", required=True, type=str)