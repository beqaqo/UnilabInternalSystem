import re
from email_validator import validate_email
from app.models.user import User, Region, City, University

def id_validator(data):
    if data.isdecimal() and len(data) == 11:
        return True


def name_validator(data):
    pattern = r'^[\u10A0-\u10FF]+$'
    return bool(re.match(pattern, data))


def mail_validator(data):
    try:
        emailObject = validate_email(data)
        return True
    except:
        return False


def number_validator(data):
    if data.isdecimal() and len(data) == 9:
        return True


def user_exist_check(parser, User):
    if User.query.filter_by(email=parser["email"]).first():
        return "მეილი უკვე გამოყენებულია", 400

    if User.query.filter_by(number=parser["number"]).first():
        return "მომხმარებელი მითითებული ნომრით უკვე არსებობს", 400

    if User.query.filter_by(personal_id=parser["personal_id"]).first():
        return "მომხმარებელი მითითებული პირადობით უკვე არსებობს", 400

    
def location_id_validator(data, model):
    return model.query.filter_by(id=data).first()
    

def parent_validator(data_1, data_2, model, parent):
    try:
        model_data = model.query.filter_by(id=data_1).first()
        
        attribute_name = f"{parent}_id" 
        if hasattr(model_data, attribute_name):
            attribute_value = getattr(model_data, attribute_name)

        if model_data and attribute_value == data_2:
            return True
        else:
            return False
    except:
        return False  
    

def check_validators(parser, user_check=True, role_check=True, terms_check=True):

    if not name_validator(parser["firstname"]):
        return "სახელი უნდა შეიცავდეს მხოლოდ ქართულ ასოებს", 400

    if not name_validator(parser["surname"]):
        return "სახელი უნდა შეიცავდეს მხოლოდ ქართულ ასოებს", 400

    if not mail_validator(parser["email"]):
        return "მეილი არ არის მითითებული სწორი ფორმით",   400

    if not number_validator(parser["number"]):
        return "ნომერი უნდა შედგებოდეს 9 რიცხვისგან",   400

    if not id_validator(parser["personal_id"]):
        return "პირადობის ნომერი უნდა შედგებოდეს 11 რიცხვისგან", 400

    if not location_id_validator(parser["region_id"], Region):
        return "მითითებული რეგიონი ვერ მოიძებნა", 400
    
    if not location_id_validator(parser["city_id"], City):
        return "მითითებული ქალაქი ვერ მოიძებნა", 400
    
    if not location_id_validator(parser["university_id"], University):
        return "მითითებული უნივერსიტეტი ვერ მოიძებნა", 400
    
    if not parent_validator(parser["city_id"], parser["region_id"], City, "region"):
        return "ქალაქი და რეგიონი არ ემთხვევა", 400

    if not parent_validator(parser["university_id"], parser["city_id"], University, "city"):
        return "უნივერსიტეტი და ქალაქი არ ემთხვევა", 400
    
    if role_check:
        if parser["role_id"] not in [2, 5]:
            return "მითითებული როლი არ არის სწორი", 400

        if parser["role_id"] == 5 and not name_validator(parser["parent_name"]):
            return "მშობლის სახელი უნდა შეიცავდეს მხოლოდ ქართულ სიმბოლოებს", 400

        if parser["role_id"] == 5 and not name_validator(parser["parent_lastname"]):
            return "მშობლის გვარი უნდა შეიცავდეს მხოლოდ ქართულ სიმბოლოებს", 400

        if parser["role_id"] == 5 and not number_validator(parser["parent_number"]):
            return "მშობლის ნომერი უნდა შედგებოდეს 9 რიცხვისგან", 400

    if user_check:
        return user_exist_check(parser, User)
