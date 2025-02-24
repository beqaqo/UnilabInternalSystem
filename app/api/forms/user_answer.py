from flask_restx import Resource, reqparse
from flask_jwt_extended import jwt_required, current_user

from app.api.forms import form_ns
from app.models.user import UserAnswer
from app.api.validators.questions import validate_user_answer

@form_ns.route("/user_answers")
class UserAnswerApi(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("form_id", required=False, type=int)
    parser.add_argument("answer_data", required=False, action="append", type=dict)

    @jwt_required()
    @form_ns.doc(security='JsonWebToken')
    def get(self):
        if current_user and current_user.is_admin():
            user_answers = UserAnswer.query.filter_by(user_id=current_user.id).all()

            user_answers_data = [answer.to_json() for answer in user_answers]

            return user_answers_data

        return "Bad request", 400

    @jwt_required()
    @form_ns.doc(security='JsonWebToken')
    def post(self):
        request_parser = self.parser.parse_args()
        data = request_parser["answer_data"]

        for answer_data in data:
            response = validate_user_answer(answer_data, request_parser["form_id"])
            if response:
                return response

            answer_is_correct = False

            correct_answer = UserAnswer.get_correct_answer(answer_data["question_id"])
            if correct_answer.text == answer_data["answer"]:
                answer_is_correct = True

            new_user_answer = UserAnswer(
                user_id=current_user.id,
                form_id=request_parser["form_id"],
                question_id=answer_data["question_id"],
                answer=answer_data["answer"],
                is_correct=answer_is_correct
            )
            new_user_answer.create()
            new_user_answer.save()

        return "Success saved User answers", 200