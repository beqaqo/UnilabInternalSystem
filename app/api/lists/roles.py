from flask_restx import Resource

from app.api.lists import lists_ns
from app.models import Role

@lists_ns.route('/roles')
class RoleApi(Resource):
    def get(self):
        return Role.get_roles()