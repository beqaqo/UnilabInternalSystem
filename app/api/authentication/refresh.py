from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from flask_restx import Resource

from app.api.authentication import auth_ns

@auth_ns.route('/refresh')
class AccessTokenRefreshApi(Resource):
    @jwt_required()
    @auth_ns.doc(security='JsonWebToken')
    def post(self):
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity)
        response = {
            "access_token": access_token
        }

        return response
