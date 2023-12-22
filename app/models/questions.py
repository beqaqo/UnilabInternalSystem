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
    form_id = db.Column(db.Integer, db.ForeignKey("forms.id"))

    option = db.relationship("QuestionOption", backref="question")
    form = db.relationship("Form", back_populates="questions")


class QuestionOption(BaseModel):
    __tablename__ = "question_options"

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey("questions.id"))
    text = db.Column(db.String, nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)

    def to_json(self):
        question_options = QuestionOption.query.filter_by(question_id=self.id).all()
        options = [
            {"text": option.text, "is_correct": option.is_correct}
            for option in question_options
        ]

        question_data = {
            "id": self.id,
            "question_text": self.question_text,
            "question_description": self.question_description,
            "question_type": self.question_type,
            "min_grade": self.min_grade,
            "min_grade_text": self.min_grade_text,
            "max_grade": self.max_grade,
            "max_grade_text": self.max_grade_text,
            "options": options,
        }

        return question_data

class Form(BaseModel):
    __tablename__ = "forms"

    id = db.Column(db.Integer, primary_key=True)
    # question_id = db.Column(db.JSON, nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey("questions.id"))
    subject = db.Column(db.String, nullable=False)
    activity_type = db.Column(db.String, nullable=False)

    questions = db.relationship("Question", back_populates="form")
