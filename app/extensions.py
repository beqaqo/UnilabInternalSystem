from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_jwt_extended import JWTManager
from flask_restx import Api


from app.config import Config


db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
jwt = JWTManager()
api = Api(
    title='UnilabInternalSystem',
    version='1.0',
    description='UnilabInternalSystem API',
    authorizations=Config.AUTHORIZATION
)

