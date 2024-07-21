from flask_restx import reqparse
from app.extensions import api

mail_ns = api.namespace('Mail', path='/api', description='Api endpoint for mail related operations')

parser = reqparse.RequestParser()
parser.add_argument("email", required=True, type=str)