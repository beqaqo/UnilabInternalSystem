from app.extensions import db
from app.models.base import BaseModel 


class Announcement(BaseModel):
    #ენაუნსმენთი ასოციაციური თეიბლია?

    __tablename__ ="announcements"
     
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.id"))
    activity_type_id = db.Column(db.Integer, db.ForeignKey("activity_type.id"))
    lecturer_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    regitration_start = db.Column(db.Date)  #?
    regitration_end = db.Column(db.Date)    #?  



class Subject(BaseModel):
    __tablename__ = "subjects" 

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)


class ActivityType(BaseModel):
    __tablename__ = "activity_type"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

