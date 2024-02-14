from app.extensions import db
from app.models.base import BaseModel

from app.models.user import User


class Portfolio(BaseModel):
    __tablename__ = "portfolios"
    id = db.Column(db.Integer, primary_key=True)
    user_uuid = db.Column(db.String, db.ForeignKey("users.uuid"))
    email = db.Column(db.String)
    fullname = db.Column(db.String)
    role = db.Column(db.String)
    about_me = db.Column(db.String)

    
    @classmethod
    def get_portfolio_data(cls, uuid):
        query = cls.query.filter_by(user_uuid=uuid).first()

        if query:
            user = User.query.filter_by(uuid=uuid).first()

            data = {
                "id": query.id,
                "user_uuid": query.user_uuid,
                "email": query.email,
                "fullnane": query.fullname,
                "role": query.role,
                "about_me": query.about_me,
                "projects": [project.to_json(user.id) for project in user.projects]
            }

            return data