from email_validator import validate_email


def id_validator(data):
    if str(data).isdecimal() and len(str(data)) == 11:
        return True
    

def name_validator(data):
    if str(data).isalpha():
        return True


def mail_validator(data):

    try:
        emailObject = validate_email(str(data))
        return True

    except :
        return False
        
     
def number_validator(data):
    if str(data).isdecimal() and len(str(data)) == 9:
        return True





def check_validators(parser):

        if not name_validator(parser["name"]):
            return "Invalid name", 400

        if not name_validator(parser["lastname"]):
            return "Invalid lastname", 400

        if not mail_validator(parser["email"]):
            return "Invalid email",   400

        if not number_validator(parser["number"]):
            return "Invalid number",   400     

        if not id_validator(parser["personal_ID"]):
            return "Invalid personal_ID", 400

        if parser["role"] == "მოსწავლე" and not name_validator(parser["parent_name"]):
            return "Invalid parent_name", 400

        if parser["role"] == "მოსწავლე" and not name_validator(parser["parent_lastname"]):
            return "Invalid parent_lastname", 400

        if parser["role"] == "მოსწავლე" and not number_validator(parser["parent_number"]):
            return "Invalid parent_number", 400




