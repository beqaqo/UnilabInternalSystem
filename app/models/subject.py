from app.extensions import db
from app.models import BaseModel

class Subject(BaseModel):
    __tablename__ = "subjects"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    course_syllabus = db.Column(db.String, nullable=True)
    internship_syllabus = db.Column(db.String, nullable=True)
    tlt_syllabus = db.Column(db.String, nullable=True)
    school_syllabus = db.Column(db.String, nullable=True)
    # Additional Links
    
    lecturers = db.relationship("User", secondary="subject_lecturer", back_populates="subjects")


class SubjectLecturer(BaseModel):
    __tablename__ = "subject_lecturer"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.id"))