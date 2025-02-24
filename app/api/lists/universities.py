from flask_restx import Resource

from app.api.lists import lists_ns
from app.models import University

@lists_ns.route('/universities/<int:city_id>')
class UniversityApi(Resource):
    def get(self, city_id):
        return University.get_universities(city_id)
