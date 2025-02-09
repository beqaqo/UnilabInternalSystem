from email_validator import validate_email
from app.models.user import User, Region, City, University

def id_validator(data):
    if data.isdecimal() and len(data) == 11:
        return True


def name_validator(data):
    if data.isalpha():
        return True


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
        return "This mail is already redgistered", 400

    if User.query.filter_by(number=parser["number"]).first():
        return "This number is already redgistered", 400

    if User.query.filter_by(personal_id=parser["personal_id"]).first():
        return "This personal_id is already redgistered", 400

    
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

    if not name_validator(parser["name"]):
        return "Invalid name", 400

    if not name_validator(parser["lastname"]):
        return "Invalid lastname", 400

    if not mail_validator(parser["email"]):
        return "Invalid email",   400

    if not number_validator(parser["number"]):
        return "Invalid number",   400

    if not id_validator(parser["personal_id"]):
        return "Invalid personal_id", 400
    
    if not location_id_validator(parser["country_id"], Country):
        return "Invalid country", 400
    
    if not location_id_validator(parser["region_id"], Region):
        return "Invalid region", 400
    
    if not location_id_validator(parser["city_id"], City):
        return "Invalid city", 400
    
    if not location_id_validator(parser["university_id"], University):
        return "Invalid university", 400
    
    if not parent_validator(parser["region_id"], parser["country_id"], Region, "country"):
        return "Region and Country doesn't match", 400
    
    if not parent_validator(parser["city_id"], parser["region_id"], City, "region"):
        return "City and Region doesn't match", 400

    if not parent_validator(parser["university_id"], parser["city_id"], University, "city"):
        return "University and City doesn't match", 400
    
    if role_check:
        if parser["role_id"] not in [2, 5]:
            return "Invalid role_id", 400

        if parser["role_id"] == 5 and not name_validator(parser["parent_name"]):
            return "Invalid parent_name", 400

        if parser["role_id"] == 5 and not name_validator(parser["parent_lastname"]):
            return "Invalid parent_lastname", 400

        if parser["role_id"] == 5 and not number_validator(parser["parent_number"]):
            return "Invalid parent_number", 400
    
    # terms არ არის userprofile -ს PUT -ში, ამიტომ საჭიროა განცალკევება
    if terms_check:
        if not parser["terms"]:
            return "Not accepted terms of service", 400

    if user_check and parser["password"] != parser["conf_password"]:
        return "Passwords do not match", 400

    if user_check:
        return user_exist_check(parser, User)
