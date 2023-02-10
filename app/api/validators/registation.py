


def id_validator(data):
    if str(data).isdecimal() and len(str(data)) == 11:
        return True
    



def name_validator(data):
    if str(data).isalpha():
        return True




def mail_validator(data):
    mails = ["gmail.com", "mail.ru", "iliauni.edu.ge"]

    if "@" in str(data):
        prefix = str(data).split("@")

        if len(prefix) == 2 and prefix[-1] in mails:

            return True
        
    
    
def number_validator(data):
    if str(data).isdecimal() and len(str(data)) == 9:
        return True


