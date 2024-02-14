from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, current_user

from app.models import Portfolio


class PortfolioApi(Resource):
    parser = reqparse.RequestParser()   
    parser.add_argument("user_uuid", required=True, type=str)
    parser.add_argument("email", required=True, type=str)
    parser.add_argument("fullname", required=True, type=str)
    parser.add_argument("role", required=True, type=str)
    parser.add_argument("about_me", required=True, type=str)

    @jwt_required()
    def get(self, uuid):
        portfolio = Portfolio.query.filter_by(user_uuid=uuid).first()

        if portfolio:
            portfolio_data = Portfolio.get_portfolio_data(uuid)

            return portfolio_data, 200
        
        return "Failed to find the portfolio", 400
    
    @jwt_required()
    def post(self):
        request_parser = self.parser.parse_args()

        portfolio = Portfolio(
            user_uuid=request_parser["user_uuid"],
            email=request_parser["email"],
            fullname=request_parser["fullname"],
            role=request_parser["role"],
            about_me=request_parser["about_me"]
        )
        portfolio.create()
        portfolio.save()

        return "Portfolio was created", 200