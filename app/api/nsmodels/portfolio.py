from flask_restx import  fields
from app.extensions import api


portfolio_ns = api.namespace('Portfolio', description='Api endpoint for User Portfolio related operations', path="/api")

portfolio_model = api.model('Portfolio', {
    'fullname': fields.String(required=True, description='Full name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'role': fields.String(required=True, description='Role of the user in the project'),
    'about_me': fields.String(required=True, description='About me section of the user'),
    'projects': fields.List(fields.Raw, description='List of projects')
})

