from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User
from app.models.questions import Question, QuestionOption


class CreateQuestion(Resource):
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

        parser = reqparse.RequestParser()
        parser.add_argument("question_text", required=True, type=str)
        parser.add_argument("question_description", required=True, type=str)
        parser.add_argument("question_type", required=True, type=str)
        parser.add_argument("min_grade", required=True, type=int)
        parser.add_argument("min_grade_text", required=True, type=str)
        parser.add_argument("max_grade", required=True, type=int)
        parser.add_argument("max_grade_text", required=True, type=str)
        parser.add_argument("option", required=True, type=dict)
        request_parser = parser.parse_args()


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
        






        
