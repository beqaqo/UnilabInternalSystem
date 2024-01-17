from app.extensions import db
from app.models.base import BaseModel


class AnnouncementUser(BaseModel):
    __tablename__ = "announcement_user"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    announcement_id = db.Column(db.Integer, db.ForeignKey("announcements.id"))
    passed = db.Column(db.Boolean, default=False)


class Announcement(BaseModel):

    __tablename__ = "announcements"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.id"))
    activity_type_id = db.Column(db.Integer, db.ForeignKey("activity_type.id"))
    lecturer_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    registration_start = db.Column(db.Date)  # ?
    registration_end = db.Column(db.Date)  # ?
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)

    projects = db.relationship("Project", back_populates="announcement")
    certificates = db.relationship("Certificate", back_populates="announcement")

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "subject_id": self.subject_id,
            "activity_type_id": self.activity_type_id,
            "lecturer_id": self.lecturer_id,
            "registration_start": str(self.registration_start),
            "registration_end": str(self.registration_end),
            "start_date": str(self.start_date),
            "end_date": str(self.end_date),
        }


class AnnouncementForm(BaseModel):

    __tablename__ = "announcements_form"

    id = db.Column(db.Integer, primary_key=True)
    announcement_id = db.Column(db.Integer, db.ForeignKey("announcements.id"))
    form_id = db.Column(db.Integer, db.ForeignKey("forms.id"))

    def to_json(self):
        return {
            "id": self.id,
            "announcement_id": self.announcement_id,
            "form_id": self.form_id
        }


class Subject(BaseModel):
    __tablename__ = "subjects"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)


class ActivityType(BaseModel):
    __tablename__ = "activity_type"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
