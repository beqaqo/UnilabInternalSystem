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
    parser.add_argument("options", required=True, action="append", type=dict)
    
    parser.add_argument("form_id", required=True, type=int)

    @jwt_required()
    def get(self):
        if not current_user.check_permission("can_create_questions"):
            return "You can't create questions", 400
    
        questions = Question.query.filter_by(user_id=current_user.id).all()

        if not questions:
            return "You don't have any question", 200

        questions = Question.get_all_questions(current_user.id)

        return questions, 200

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
            form_id=request_parser["form_id"]
        )
        new_question.create()
        new_question.save()  

        for option in request_parser["options"]:        
            new_option = QuestionOption(
                question_id=new_question.id,
                text=option["text"],
                is_correct=option["is_correct"],
            )

            new_option.create()
            new_option.save()

        return "success", 200
    

class FormApi(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument("question_id", required=False, type=int)
    parser.add_argument("subject", required=True, type=int)
    parser.add_argument("activity_type", required=True, type=int)

    @jwt_required()
    def get(self):
        forms = Form.query.filter_by(user_id=current_user.id).all()

        if not forms:
            return "You don't have any forms", 200

        forms_data = Form.get_forms(current_user.id)

        return forms_data, 200
    
    @jwt_required()
    def post(self):
        request_parser = self.parser.parse_args()
        
        if not current_user.check_permission("can_create_forms"):
            return "Bad request", 400
          
        form = Form(
            user_id=current_user.id,
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
    parser.add_argument("answer_data", required=False, action="append", type=dict)

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

        for answer_data in data:
            response = validate_user_answer(answer_data)
            if response:
                return response
            
            answer_is_correct = False

            correct_answer = UserAnswer.get_correct_answer(answer_data["question_id"])
            if correct_answer.text == answer_data["answer"]:
                answer_is_correct = True

            new_user_answer = UserAnswer(
                user_id=current_user.id,
                form_id=answer_data["form_id"],
                question_id=answer_data["question_id"],
                answer=answer_data["answer"],
                is_correct=answer_is_correct
            )
            new_user_answer.create()
            new_user_answer.save()

        return "Success", 200
