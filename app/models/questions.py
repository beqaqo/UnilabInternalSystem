from app.extensions import db
from app.models.base import BaseModel


class Question(BaseModel):
    __tablename__ = "questions"

    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.String, nullable=False)
    question_description = db.Column(db.String)
    question_type = db.Column(db.String)
    min_grade = db.Column(db.Integer)
    min_grade_text = db.Column(db.String)
    max_grade = db.Column(db.Integer)
    max_grade_text = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    option = db.relationship("QuestionOption", backref="question")


class QuestionOption(BaseModel):
    __tablename__ = "question_options"

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey("questions.id"))
    text = db.Column(db.String, nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)

    def to_json(self):
        return {
            "id": self.id,
            "question_id": self.question_id,
            "text": self.text,
            "is_correct": self.is_correct
        }
