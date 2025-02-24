from flask_restx import Resource

from app.api.lists import lists_ns
from app.models import School

@lists_ns.route('/schools/<int:city_id>')
class SchoolApi(Resource):
    def get(self, city_id):
        return School.get_schools(city_id)