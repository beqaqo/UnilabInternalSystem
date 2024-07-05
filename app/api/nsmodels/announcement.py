from flask_restx import  reqparse, inputs, fields
from app.extensions import api

announcement_ns = api.namespace('Announcement', description = 'გამოცხადებულ კურსებთან დაკავშირებული ოპერაციები',path ='/api')


# announcement_model = announcement_ns.model('Announcement',{
#     'name':fields.String(required = True, description = 'კურსის სახელი', example = 'შესავალი პითონში' ),
#     'subjects_id':fields.Integer(required = True, description = 'საგნის ID ', example = 1 ),
#     'activity_type_id':fields.String(required = True , description = 'აქტივობის ტიპის ID', example = 1),
#     'registration_start': fields.DateTime(required = True, description='რეგისტრაციის დაწყების დრო', dt_format='iso8601',example='2024-06-25T15:22:57.338Z' ),
#     'registration_end': fields.DateTime(required = True, description ='რეგისტრაციის დასასრულის დრო', dt_format='iso8601',example='2024-06-25T15:22:57.338Z'),
#     'start_date': fields.DateTime(required = True, description = 'კურსის დაწყების თარიღი' ,dt_format='iso8601',example='2024-06-25T15:22:57.338Z'),
#     'end_date': fields.DateTime(required = True, description = 'კურსის დამთავრების თარიღი',dt_format='iso8601',example='2024-06-25T15:22:57.338Z')

# })


announcement_parser = reqparse.RequestParser()
announcement_parser.add_argument("name", required=True, type=str)
announcement_parser.add_argument("subject_id", required=True, type=int)
announcement_parser.add_argument("activity_type_id", required=True, type=int)
announcement_parser.add_argument("lecturer_ids", required=True, action="append", type=dict)
# announcement_parser.add_argument("registration_start", required=True, type=inputs.datetime_from_iso8601)
# announcement_parser.add_argument("registration_end", required=True, type=inputs.datetime_from_iso8601)
announcement_parser.add_argument("start_date", required=True, type=inputs.datetime_from_iso8601)
announcement_parser.add_argument("end_date", required=True, type=inputs.datetime_from_iso8601)
announcement_parser.add_argument("description", required=False, type=str)