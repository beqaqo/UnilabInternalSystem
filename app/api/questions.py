from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, current_user
from app.models.user import User, UserAnswer
from app.models.questions import Question, QuestionOption, Form
from app.api.validators.questions import validate_user_answer


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
        if not current_user.check_permission("can_create_questions"):
            return "Bad request", 400

        questions = Question.query.filter_by(user_id=current_user.id).all()

        if not questions:
            return "You don't have any question", 200

        questions_with_options = [question.to_json() for question in questions]

        return questions_with_options, 200

    @jwt_required()
    def post(self):

        request_parser = self.parser.parse_args()

        if not current_user.check_permission("can_create_questions"):
            return "Bad request", 400

        new_question = Question(
            user_id=current_user.id,
            question_text=request_parser["question_text"],
            question_description=request_parser["question_description"],
            question_type=request_parser["question_type"],
            min_grade=request_parser["min_grade"],
            min_grade_text=request_parser["min_grade_text"],
            max_grade=request_parser["max_grade"],
            max_grade_text=request_parser["max_grade_text"],

        )
        new_question.create()
        new_question.save()

        for option in request_parser["option"].keys():
            new_option = QuestionOption(
                question_id=new_question.id,
                text=option,
                is_correct=request_parser["option"][option],
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
        forms = Form.query.filter_by(user_id=current_user.id).all()

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
        
        if not current_user.check_permission("can_create_forms"):
            return "Bad request", 400
          
        form = Form(
            user_id=current_user.id,
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
        
        if not current_user.check_permission("can_create_forms"):
            return "Bad request", 400
        
        form = Form.query.filter_by(user_id=current_user.id).first()
        if not form:
            return "Form not found", 404

        form.question_id = request_parser["question_id"]
        form.subject = request_parser["subject"]
        form.activity_type = request_parser["activity_type"]
        form.save()

        return "success", 200


class UserAnswerApi(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument("answer_data", required=True, type=list)

    @jwt_required()
    def get(self):
        if current_user and current_user.is_admin():
            request_parser = self.parser.parse_args()

            return request_parser
        else:
            return "Bad request", 400

    @jwt_required()
    def post(self):
        request_parser = self.parser.parse_args()
        data = request_parser["answer_data"]

        response = validate_user_answer(data)
        if response:
            return response

        for answer_data in data:
            answer_is_correct = False

            correct_answer = UserAnswer.get_correct_answer(answer_data["question_id"])
            if correct_answer.text == answer_data["answer"]:
                answer_is_correct = True

            new_user_answer = UserAnswer(
                user_id=current_user.user_id,
                form_id=answer_data["form_id"],
                question_id=answer_data["question_id"],
                answer=answer_data["answer"],
                is_correct=answer_is_correct
            )
            new_user_answer.create()
            new_user_answer.save()

        return "Success", 200
