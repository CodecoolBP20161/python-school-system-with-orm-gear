
from model.City import City
# from model.InterviewSlotMentor import InterviewSlotMentor
from model.Person import Person
# from controll_admin import Person, City, InterviewSlotMentor
from datetime import *
from peewee import CharField, TextField, DateTimeField

import random


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
                school_get = City.get(City.applicant_city == applicant.city)
                applicant.school = school_get.school
                applicant.save()

    # @classmethod
    # def update_applicant(cls):
    #     new_applicant = cls.select().join(City, on=City.applicant_city == cls.city).where(cls.status == "new")
    #     for applicant in new_applicant:
    #         applicant.update_school()

    @classmethod
    def get_codes(cls):
        codes = []
        get_codes = cls.select(cls.code).where(~(cls.code >> None)).tuples()
        for code in get_codes:
            codes.append(codes)
        return codes

    def new_code(self):
        while True:
            new_code = "".join([self.school[:2].upper(), str(random.randint(1000, 10000))])
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

    def get_mentors_for_interview(self):
        mentors = []


        # for mentor in InterviewSlotMentor.select():
        #     if applicant.id == mentor.interview.id:
        #         mentors.append(mentor.mentor.first_name)
        #         mentors.append(mentor.mentor.last_name)


        return mentors

    @classmethod
    def create_from_form(cls, request_form):
        return Applicant(first_name=request_form['first_name'],
                         last_name=request_form['last_name'],
                         email=request_form['email'],
                         city=request_form['city'])

    def valid(self):
        from validation import Validation
        errors = {}
        if Validation.first_name_validation(self.first_name):
            errors['first_name'] = 'Invalid'
        if Validation.last_name_validation(self.last_name):
            errors['last_name'] = 'Invalid'
        if Validation.email_exists(self.email):
            errors['email'] = 'already in use'
        return errors

    # @classmethod
    # def mentors_for_applicant(cls, first_name, last_name):
    #     return cls.select(Applicant, InterviewSlot, InterviewSlotMentor, Mentor).join(
    #         InterviewSlot).join(
    #         InterviewSlotMentor).join(Mentor).where(Mentor.first_name.contains(first_name),
    #                                                 Mentor.last_name.contains(last_name))
