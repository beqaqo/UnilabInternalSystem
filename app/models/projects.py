from app.extensions import db
from app.models.base import BaseModel


class Project(BaseModel):

    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String)
    url = db.Column(db.String)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("User", back_populates="projects")

    announcement_id = db.Column(db.Integer, db.ForeignKey("announcements.id"))
    announcement = db.relationship("Announcement", back_populates="projects")
