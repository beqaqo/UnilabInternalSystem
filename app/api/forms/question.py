from flask_restx import Resource, reqparse
from flask_jwt_extended import jwt_required, current_user

from app.api.forms import form_ns
from app.models.questions import Question, QuestionOption

@form_ns.route("/question")
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

    @jwt_required()
    @form_ns.doc(security='JsonWebToken')
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("question_id", required=False, type=str, location="args")
        received_arguments = parser.parse_args()

        if not current_user.check_permission("can_view_questions"):
            return "You can't view questions", 400

        questions = Question.query.filter_by(user_id=current_user.id).all()

        if not questions:
            return "You don't have any questions", 200

        if received_arguments["question_id"]:
            questions = Question.get_all_questions(current_user.id, received_arguments["question_id"])
        else:
            questions = Question.get_all_questions(current_user.id)

        return questions, 200

    @jwt_required()
    @form_ns.doc(security='JsonWebToken')
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

        for option in request_parser["options"]:
            new_option = QuestionOption(
                question_id=new_question.id,
                text=option["text"],
                is_correct=option["is_correct"],
            )

            new_option.create()
        new_option.save()

        return "Successfully saved Questions", 200