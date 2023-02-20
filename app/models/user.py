from app.extensions import db
from app.models.base import BaseModel
from werkzeug.security import generate_password_hash, check_password_hash


class User(BaseModel):

    __tablename__ = "Users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    lastname = db.Column(db.String)
    email = db.Column(db.String)
    _password = db.Column("password", db.String)
    personal_id = db.Column(db.String)
    number = db.Column(db.String)
    date = db.Column(db.Date)
    gender = db.Column(db.String)
    country = db.Column(db.String)
    region = db.Column(db.String)
    city = db.Column(db.String)
    address = db.Column(db.String)
    role = db.Column(db.String)
    confirmed = db.Column(db.Integer, unique=False, default=False)
    reset_password = db.Column(db.Integer, unique=False, default=False)



    # Pupil
    school = db.Column(db.String)
    grade = db.Column(db.String)
    parent_name = db.Column(db.String)
    parent_lastname = db.Column(db.String)
    parent_number = db.Column(db.String)

    # student
    university = db.Column(db.String)
    faculty = db.Column(db.String)
    program = db.Column(db.String)
    semester = db.Column(db.String)
    degree_level = db.Column(db.String)




    def _get_password(self):
        return self._password

    def _set_password(self, password):
        self._password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    password = db.synonym('_password', descriptor=property(_get_password, _set_password))