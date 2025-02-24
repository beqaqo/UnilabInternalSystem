from flask_restx import Resource, reqparse
from flask_jwt_extended import jwt_required, current_user

from app.api.forms import form_ns
from app.models.questions import Form

@form_ns.route("/form")
class FormApi(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("question_id", required=False, type=int)
    parser.add_argument("subject", required=True, type=int)
    parser.add_argument("activity_type", required=True, type=int)

    @jwt_required()
    @form_ns.doc(security='JsonWebToken')
    def get(self):
        forms_data = Form.get_forms(current_user.id)

        if not forms_data:
            return "You don't have any Forms", 404

        return forms_data, 200

    @jwt_required()
    @form_ns.doc(security='JsonWebToken')
    def post(self):
        request_parser = self.parser.parse_args()

        if not current_user.check_permission("can_create_forms"):
            return "You can't create Forms", 403

        form = Form(
            user_id=current_user.id,
            subject=request_parser["subject"],
            activity_type=request_parser["activity_type"]
        )
        form.create()
        form.save()

        return "Successfully created a Form", 200