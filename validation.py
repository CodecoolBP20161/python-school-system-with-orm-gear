from models import *
import re


class Validation:

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
    def email_exists(email):
        return Applicant.select().where(Applicant.email == email).exists()
