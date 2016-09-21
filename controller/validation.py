from model.Applicant import Applicant
import re
import json


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

    @staticmethod
    def read_login_info():
        with open('admin.json') as json_data:
            admin_data = json.load(json_data)
        return admin_data

    @staticmethod
    def username_correct(username):
        admin_data = Validation.read_login_info()
        return username == admin_data['username']

    @staticmethod
    def password_correct(password):
        admin_data = Validation.read_login_info()
        return password == admin_data['password']
