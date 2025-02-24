from flask_restx import Resource, fields

from app.extensions import api
from app.models import User, Project

portfolio_ns = api.namespace('Portfolio', description='Api endpoint for User Portfolio related operations', path="/api")

portfolio_model = api.model('Portfolio', {
    'fullname': fields.String(required=True, description='Full name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'role': fields.String(required=True, description='Role of the user in the project'),
    'about_me': fields.String(required=True, description='About me section of the user'),
    'projects': fields.List(fields.Raw, description='List of projects')
})


@portfolio_ns.route('/portfolio/<string:uuid>')
@portfolio_ns.doc(responses={200: 'OK', 400: 'Invalid Argument', 404: 'User Not Found'})
class PortfolioApi(Resource):

    @portfolio_ns.marshal_with(portfolio_model)
    def get(self, uuid):
        user: User = User.query.filter_by(uuid=uuid).first()

        if user:
            project = Project.query.join(Project.user).filter(User.uuid == uuid).first()

            data = {
                "fullname": f"{user.name} {user.lastname}",
                "email": user.email,
                "role": project.announcement.name,
                "about_me": user.about_me,
                "projects": [project.to_json(user.id) for project in user.projects]
            }

            return data, 200

        return "Invalid user", 400