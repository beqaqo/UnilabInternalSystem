from flask_restx import Resource
from app.extensions import api

from app.models import User, Project
from app.api.nsmodels import portfolio_ns, portfolio_model


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
    