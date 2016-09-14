from peewee import *
from model.Person import Person
from model.BaseModel import BaseModel
from model.City import *
from model.Mentor import *
from model.InterviewSlotMentor import *
from model.InterviewSlot import *
from datetime import *
import random


class Applicant(Person):
    code = CharField(default=None, null=True, unique=True)
    city = TextField()
    status = CharField(default='new')
    registration_time = DateTimeField(default=datetime.utcnow())

    @classmethod
    def new_applicant(cls):
        return cls.select().where(cls.status == "new")

    def update_school(self):
        school_get = City.get(City.applicant_city == self.city).school
        self.school = school_get
        self.save()

    def generate_code(self):
        get_codes = Applicant.select().where(~(Applicant.code >> None))
        if get_codes:
            not_unique = True
            while not_unique is True:
                new_code = "".join([self.city[:2].upper(), str(random.randint(1000, 10000))])
                for code in get_codes:
                    if new_code not in code.code:
                        not_unique = False
            self.code = new_code
            self.save()
        else:
            new_code = "".join([self.city[:2].upper(), str(random.randint(1000, 10000))])
            self.code = new_code
            self.save()

    @classmethod
    def get_assigned_applicants(cls):
        return cls.select().where(~(cls.code >> None), ~(cls.school >> None), cls.status == "new")

    @classmethod
    def get_interviewed_applicant(cls):
        return cls.select().where(cls.status == "processing")

    def get_mentors_for_interview(self, query):
        mentors = []
        for applicant in self.applicant_datas:
            if query == "time":
                return applicant.time
            for mentor in InterviewSlotMentor.select():
                if applicant.id == mentor.interview.id:
                    mentors.append(mentor.mentor.first_name)
                    mentors.append(mentor.mentor.last_name)
                    # print(mentor.mentor.first_name, mentor.mentor.last_name)
        if query == "mentors":
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
            errors['first_name'] = 'Invalid first name'
        if Validation.last_name_validation(self.last_name):
            errors['last_name'] = 'Invalid last name'
        if Validation.email_exists(self.email):
            errors['email'] = 'E-mail already in use'
        return errors

    @classmethod
    def mentors_for_applicant(cls, first_name, last_name):
        return cls.select(Applicant, InterviewSlot, InterviewSlotMentor, Mentor).join(
            InterviewSlot).join(
            InterviewSlotMentor).join(Mentor).where(Mentor.first_name.contains(first_name),
                                                    Mentor.last_name.contains(last_name))


    @classmethod
    def option_groups(cls, groups):
        result = []
        for group in groups:
            attribute = getattr(cls, group)
            result.append(cls.select(attribute).group_by(attribute))
        return result