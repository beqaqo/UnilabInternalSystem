from flask_restx import  reqparse
from app.extensions import api


subjects_ns = api.namespace('Subjects', description='Api endpoint for User Profile related operations', path="/api")

subjects_parser = reqparse.RequestParser()

subjects_parser.add_argument('name', type=str, required=True, help='Subject name: C++')
subjects_parser.add_argument('lecturers_id', type=int, action='append', required=True, help='The unique identifier of a lecturer example - 3')
subjects_parser.add_argument('course_syllabus', type=str, required=True, help='Example syllabus.pdf')
subjects_parser.add_argument('internship_syllabus', type=str, required=True, help='Example syllabus.pdf')
subjects_parser.add_argument('tlt_syllabus', type=str, required=True, help='Example syllabus.pdf')
subjects_parser.add_argument('school_syllabus', type=str, required=True, help='Example syllabus.pdf')