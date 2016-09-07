from models import *
import re


class Validation:
    """ validate first_name last_name are contains numbers and validation for e-mail is not contain @ or .
        the instance methods will return True if the validation is OK or False if it is not valid
        Usage:
        email = Validation("Jozsi", "Mari", "ggg@gmail.com")
        print(email.first_name_validation())
        print(email.last_name_validation())
        print(email.e_mail_validation())"""

    # def __init__(self, first_name, last_name, e_mail):
    #     self.first_name = first_name
    #     self.last_name = last_name
    #     self.e_mail = e_mail

    @staticmethod
    def first_name_validation(first_name):
        for letter in first_name:
            if letter.isdigit():
                return True
        return False

    @staticmethod
    def last_name_validation(last_name):
        for letter in last_name:
            if letter.isdigit():
                return True
        return False

    @staticmethod
    def email_validation(email):
        email_from_database = Applicant.select('email').where(Applicant.email == email)
        return email == email_from_database

    # def email_validation(applicant, email):
    #     row = applicant.select().where(applicant.email == email)
    #     print(row)
    #     try:
    #         extracted_email = row.get(email)
    #         print(extracted_email)
    #         if extracted_email == email:
    #             return False
    #         else:
    #             return True
    #     except:
    #         print("No matching row is found")
