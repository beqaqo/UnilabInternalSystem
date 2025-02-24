from flask_restx import Resource

from app.api.lists import lists_ns
from app.models import Region

@lists_ns.route('/locations')
class LocationApi(Resource):
    def get(self):
        return Region.get_locations()