from flask_restx import reqparse
from app.extensions import api


certificate_ns = api.namespace('Certificate', path='/api')

parser = reqparse.RequestParser()
parser.add_argument("user_id", required=True, type=str)
parser.add_argument("announcement_id", required=True, type=str)