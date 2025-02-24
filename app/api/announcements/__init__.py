from flask_restx import fields, reqparse, inputs
from app.extensions import api

announcement_ns = api.namespace('Announcement', description = 'გამოცხადებულ კურსებთან დაკავშირებული ოპერაციები',path ='/api')

announcement_model = announcement_ns.model('Announcement', {
    'name': fields.String(required=True, description='კურსის სახელი', example='შესავალი პითონში'),
    'subject_id': fields.Integer(required=True, description='საგნის ID', example=1),
    'lecturer_ids': fields.List(fields.Integer, required=True, description='Lecturer IDs for the announcement'),
    'activity_type_id': fields.String(required=True, description='აქტივობის ტიპის ID', example='1'),
    'registration_start': fields.DateTime(required=True, description='რეგისტრაციის დაწყების დრო', dt_format='iso8601', example='2024-06-25T15:22:57.338Z'),
    'registration_end': fields.DateTime(required=True, description='რეგისტრაციის დასასრულის დრო', dt_format='iso8601', example='2024-06-25T15:22:57.338Z'),
    'start_date': fields.DateTime(required=True, description='კურსის დაწყების თარიღი', dt_format='iso8601', example='2024-06-25T15:22:57.338Z'),
    'end_date': fields.DateTime(required=True, description='კურსის დამთავრების თარიღი', dt_format='iso8601', example='2024-06-25T15:22:57.338Z')
})

parser = reqparse.RequestParser()
parser.add_argument("name", required=True, type=str, location='json')
parser.add_argument("subject_id", required=True, type=int, location='json')
parser.add_argument("activity_type_id", required=True, type=str, location='json')
parser.add_argument("lecturer_ids", required=True, type=list,   location='json',)
parser.add_argument("registration_start", required=True, type=inputs.datetime_from_iso8601, location='json')
parser.add_argument("registration_end", required=True, type=inputs.datetime_from_iso8601, location='json')
parser.add_argument("start_date", required=True, type=inputs.datetime_from_iso8601, location='json')
parser.add_argument("end_date", required=True, type=inputs.datetime_from_iso8601, location='json')
parser.add_argument("description", required=False, type=str, location='json')