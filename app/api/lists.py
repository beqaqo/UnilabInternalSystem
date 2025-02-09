from flask_restx import Resource, reqparse
from app.models.user import Region, City, University, School
from app.models.roles import Role
from app.extensions import api

listApi = api.namespace("lists", path='/api', description='რეგიონების, სკოლების და უნივერსიტეტების წამოღება ქალაქების მიხედვით, ყველა როლის წამოღება ადმინის გარდა')


@listApi.route('/get_locations')
class GetLocations(Resource):
    def get(self):
        return Region().get_locations()

@listApi.route('/get_universities/<int:city_id>')
class GetUniversities(Resource):
    def get(self, city_id):
        return University.get_universities(city_id)

@listApi.route('/get_schools/<int:city_id>')
class GetSchools(Resource):
    def get(self, city_id):
        return School.get_schools(city_id)

@listApi.route('/get_roles')
class GetRoles(Resource):
    def get(self):
        return Role.get_roles()
