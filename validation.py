from models import *
import re


#

class Validation:
    """ validate first_name last_name are contains numbers and validation for e-mail is not contain @ or .
        the instance methods will return True if the validation is OK or False if it is not valid
        Usage:
        email = Validation("Jozsi", "Mari", "ggg@gmail.com")
        print(email.first_name_validation())
        print(email.last_name_validation())
        print(email.e_mail_validation())"""

    def __init__(self, first_name, last_name, e_mail):
        self.first_name = first_name
        self.last_name = last_name
        self.e_mail = e_mail

    def first_name_validation(self):
        for letter in self.first_name:
            if letter.isdigit():
                return False
        return True

    def last_name_validation(self):
        for letter in self.last_name:
            if letter.isdigit():
                return False
        return True

    def e_mail_exist(self):
        try:
            e_mail_database = Applicant.get(Applicant.email == self.e_mail)
            if e_mail_database:
                return False
        except:
            print("Email is valid")
        return True



probae = Validation("sasa", "adda", "girh.cc.2016@gmail.com")
print(probae.e_mail_exist())