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

    options = db.relationship("QuestionOption", backref="question")
    forms = db.relationship("Form", back_populates="questions", secondary="question_form")

    @classmethod
    def get_all_questions(cls, user_id, question_id = None):

        questions = cls.query.filter(cls.user_id==user_id).options(db.joinedload(Question.options)).all()

        if question_id:
            questions = questions.filter(cls.id==question_id)
        
        questions = questions.options(db.joinedload(Question.options)).all()

        # questions = cls.query.filter_by(user_id=user_id).options(db.joinedload(Question.options)).all()

        all_questions = [
            {
                "id": question.id,
                "question_text": question.question_text,
                "question_description": question.question_description,
                "question_type": question.question_type,
                "min_grade": question.min_grade,
                "min_grade_text": question.min_grade_text,
                "max_grade": question.max_grade,
                "max_grade_text": question.max_grade_text,
                "user_id": question.user_id,
                "form_id": question.form_id,
                "options": [
                    {
                        "text": option.text,
                        "is_correct": option.is_correct
                    }
                    for option in question.option
                ]
            }
            for question in questions
        ]

        return all_questions

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
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    subject = db.Column(db.Integer, db.ForeignKey("subjects.id"))
    activity_type = db.Column(db.Integer, db.ForeignKey("activity_type.id"))

    questions = db.relationship("Question", back_populates="forms", secondary="question_form")

    @classmethod
    def get_forms(cls, user_id):
        form_data = cls.query.filter_by(user_id=user_id).options(db.joinedload(Form.questions)).all()

        forms = [
            {
                "subject": f.subject,
                "activity_type": f.activity_type,
                "questions": [
                    {
                        "id": question.id,
                        "question_text": question.question_text,
                        "question_description": question.question_description,
                        "question_type": question.question_type,
                        "min_grade": question.min_grade,
                        "min_grade_text": question.min_grade_text,
                        "max_grade": question.max_grade,
                        "max_grade_text": question.max_grade_text,
                        "user_id": question.user_id,
                        "form_id": question.form_id,
                    }
                    for question in f.questions
                ]
            }
            for f in form_data
        ]

        return forms
    

class QuestionForm:
    __tablename__ = "question_form"

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey("questions.id"))
    form_id = db.Column(db.Integer, db.ForeignKey("forms.id"))
