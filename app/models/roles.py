from app.extensions import db
from app.models.base import BaseModel


class UserRole(BaseModel):

    __tablename__ = "user_roles"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))



class Role(BaseModel):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    can_create_activity = db.Column(db.Boolean, default=False)
    can_create_subject = db.Column(db.Boolean, default=False)
    can_create_roles = db.Column(db.Boolean, default=False)
    can_edit_users = db.Column(db.Boolean, default=False)
    can_create_questions = db.Column(db.Boolean, default=False)
    can_view_questions = db.Column(db.Boolean, default=False)
    can_create_forms = db.Column(db.Boolean, default=False)
    can_create_certificates = db.Column(db.Boolean, default=False)

    @classmethod
    def get_roles(cls):
        roles = cls.query.filter(cls.name != "ადმინი").all()
        return [{"id": role.id, "name": role.name} for role in roles]