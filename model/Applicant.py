import random
from datetime import *

from peewee import CharField, TextField, DateTimeField

from model.City import City
from model.Person import Person


class Applicant(Person):
    code = CharField(default=None, null=True, unique=True)
    city = TextField()
    status = CharField(default='new')
    registration_time = DateTimeField(default=datetime.utcnow())

    @classmethod
    def new_applicant(cls):
        return cls.select().where(cls.status == "new")

    @classmethod
    def update_school(cls):
        new_applicant = cls.filter("status", "new")
        if new_applicant:
            for applicant in new_applicant:
                school_get = City.get(City.applicant_city == applicant.city).school
                applicant.school = school_get
                applicant.save()

    @classmethod
    def get_codes(cls):
        codes = []
        get_codes = cls.select(cls.code).where(~(cls.code >> None)).tuples()
        for code in get_codes:
            codes.append(codes)
        return codes

    def new_code(self):
        while True:
            new_code = "".join([self.city[:2].upper(), str(random.randint(1000, 10000))])
            if new_code not in Applicant.get_codes():
                break
        return new_code

    @classmethod
    def set_code(cls):
        get_applicant = cls.filter("code", None)
        for applicant in get_applicant:
            applicant.code = applicant.new_code()
            applicant.save()
            print(applicant.code, applicant.first_name, applicant.last_name, applicant.city, applicant.school,
                  applicant.status, applicant.email)

    @classmethod
    def get_assigned_applicants(cls):
        return cls.select().where(~(cls.code >> None), ~(cls.school >> None), cls.status == "new")

    def get_mentors_for_interview_time(self):
        for applicant in self.applicant_datas:
            return applicant.time


    @classmethod
    def create_from_form(cls, request_form):
        return Applicant(first_name=request_form['first_name'],
                         last_name=request_form['last_name'],
                         email=request_form['email'],
                         city=request_form['city'])

    def valid(self):
        from controller.validation import Validation
        errors = {}
        if Validation.first_name_validation(self.first_name):
            errors['first_name'] = 'Invalid first name'
        if Validation.last_name_validation(self.last_name):
            errors['last_name'] = 'Invalid last name'
        if Validation.email_exists(self.email):
            errors['email'] = 'E-mail already in use'
        return errors
