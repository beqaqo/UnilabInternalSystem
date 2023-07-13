from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User
from app.models.questions import Question, QuestionOption, Form


class QuestionApi(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument("question_text", required=True, type=str)
    parser.add_argument("question_description", required=True, type=str)
    parser.add_argument("question_type", required=True, type=str)
    parser.add_argument("min_grade", required=True, type=int)
    parser.add_argument("min_grade_text", required=True, type=str)
    parser.add_argument("max_grade", required=True, type=int)
    parser.add_argument("max_grade_text", required=True, type=str)
    parser.add_argument("option", required=True, type=dict)

    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        user = User.query.filter_by(email=current_user).first()

        if not user.check_permission("can_create_questions"):
            return "Bad request", 400
        
        questions = Question.query.filter_by(user_id=user.id).all()
    
        if not questions:
            return "You don't have any question", 200
        
        question_with_options = []

        for question in questions:
            options = QuestionOption.query.filter_by(question_id = question.id).all()
            question_options={}
            for option in options:
                question_options[option.text] = option.is_correct

            user_question = {
                "question_text" : question.question_text,
                "question_description": question.question_description,
                "question_type":question.question_type,
                "min_grade":question.min_grade,
                "min_grade_text":question.min_grade_text,
                "max_grade":question.max_grade,
                "max_grade_text":question.max_grade_text,
                "question_options": question_options
            }

            question_with_options.append(user_question)
           

        return question_with_options, 200
    


    @jwt_required()
    def post(self):

        request_parser = self.parser.parse_args()


        current_user = get_jwt_identity()
        user = User.query.filter_by(email=current_user).first()
        

        if not user.check_permission("can_create_questions"):
            return "Bad request", 400
        

        new_question = Question(
            user_id = user.id,
            question_text = request_parser["question_text"],
            question_description = request_parser["question_description"],
            question_type = request_parser["question_type"],
            min_grade = request_parser["min_grade"],
            min_grade_text = request_parser["min_grade_text"],
            max_grade = request_parser["max_grade"],
            max_grade_text = request_parser["max_grade_text"],

        )
        new_question.create()
        new_question.save()

        for option in request_parser["option"].keys():
            new_option = QuestionOption(
                question_id = new_question.id,
                text = option,
                is_correct = request_parser["option"][option],
            )
        
            new_option.create()
        new_option.save()

        return "success", 200

class FormApi(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument("question_id", required=True, type=list, help="question_id is required and should be an integer")
    parser.add_argument("subject", required=True, type=str, help="subject is required and should be an string")
    parser.add_argument("activity_type", required=True, type=str, help="activity_type is required and should be an string")

    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        user = User.query.filter_by(email=current_user).first()

        forms = Form.query.filter_by(user_id=user.id).all()

        if not forms:
            return "You don't have any forms", 200

        forms_data = []
        for form in forms:
            form_data = {
                "question_id": form.question_id,
                "subject": form.subject,
                "activity_type": form.activity_type
            }
            forms_data.append(form_data)

        return forms_data, 200
    @jwt_required()
    def post(self):
        request_parser = self.parser.parse_args()

        current_user = get_jwt_identity()
        user = User.query.filter_by(email=current_user).first()

        form = Form(
            user_id=user.id,
            question_id=request_parser["question_id"],
            subject=request_parser["subject"],
            activity_type=request_parser["activity_type"]
        )
        form.create()
        form.save()

        return "success", 200

    @jwt_required()
    def put(self):
        request_parser = self.parser.parse_args()

        current_user = get_jwt_identity()
        user = User.query.filter_by(email=current_user).first()

        form = Form.query.filter_by(user_id=user.id).first()

        if not form:
            return "Form not found", 404

        form.question_id = request_parser["question_id"]
        form.subject = request_parser["subject"]
        form.activity_type = request_parser["activity_type"]
        form.save()

        return "success", 200
        






        
