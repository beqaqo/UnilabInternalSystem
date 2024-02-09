from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, current_user
from werkzeug.datastructures import FileStorage
from flask import request
from uuid import uuid4

from app.models import Subject, SubjectLecturer
from app.config import Config


class SubjectApi(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("name", required=True, location="form")
    parser.add_argument("lecturers_id", required=True, type=int, action="append", location="form")
    parser.add_argument("course_syllabus", type=str, location="files")
    parser.add_argument("internship_syllabus", type=str, location="files")
    parser.add_argument("tlt_syllabus", type=str, location="files")
    parser.add_argument("school_syllabus", type=str, location="files")
    # Additional Links

    @jwt_required()
    def post(self):
        request_parser = self.parser.parse_args()
        syllabus_list = [
            request_parser["course_syllabus"],
            request_parser["internship_syllabus"],
            request_parser["tlt_syllabus"],
            request_parser["school_syllabus"],
        ]
        names = ["course_syllabus", "internship_syllabus", "tlt_syllabus", "school_syllabus"]

        if not current_user.check_permission("can_create_subject"):
            return "You can't create Subjects", 403

        syllabus_names = [str(uuid4()) if syllabus is not None else None for syllabus in syllabus_list]
        if not any(syllabus_list):
            return "At least one syllabus must be sent", 400
        
        for index, syllabus in enumerate(syllabus_names):
            if syllabus is not None:
                request.files[names[index]].save(f"files/{syllabus}.pdf")
                

        new_subject = Subject(
            name = request_parser["name"],
            course_syllabus = syllabus_names[0],
            internship_syllabus = syllabus_names[1],
            tlt_syllabus = syllabus_names[2],
            school_syllabus = syllabus_names[3],
            # Additional Links
        )
        new_subject.create()
        new_subject.save()

        for lecturer_id in request_parser["lecturers_id"]:
            subject_lecturer = SubjectLecturer(
                user_id = lecturer_id,
                subject_id = new_subject.id,
            )
            subject_lecturer.create()
        subject_lecturer.save()

        return "Successfully created a Subject", 200
    