from flask_restx import Resource, reqparse
from flask_jwt_extended import jwt_required, current_user

from app.api.forms import form_ns
from app.models.questions import QuestionForm

@form_ns.route("/form_questions")
class FormQuestionApi(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument("form_id", required=True, type=int)
    parser.add_argument("questions_id", required=True, type=int, action="append")

    @jwt_required()
    @form_ns.doc(security='JsonWebToken')
    def post(self):
        request_parser = self.parser.parse_args()

        if not current_user.check_permission("can_create_forms"):
            return "You can't create Question forms", 403

        for index, question_id in enumerate(request_parser["questions_id"]):
            question_form = QuestionForm(
                question_id=question_id,
                form_id=request_parser["form_id"],
                order=index + 1
            )
            question_form.create()

        question_form.save()

        return "Successfully created a Question Form", 200