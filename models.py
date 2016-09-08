from peewee import *
import random
from read_from_text import *
from datetime import *

# db = PostgresqlDatabase('6_teamwork_week', user=Read_from_text.connect_data())
db = PostgresqlDatabase('6_teamwork_week',
                        **{'user': Read_from_text.connect_data(), 'host': 'localhost', 'port': 5432,
                           'password': '753951'})


class BaseModel(Model):
    """A base model that will use our Postgresql database"""

    class Meta:
        database = db


class Person(BaseModel):
    first_name = CharField()
    last_name = CharField()
    school = CharField(default='', null=True)
    email = CharField()

    @property
    def full_name(self):
        return ' '.join([self.first_name, self.last_name])


class City(BaseModel):
    applicant_city = TextField()
    school = TextField()


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


class Mentor(Person):
    pass


class InterviewSlot(BaseModel):
    mentor = ForeignKeyField(Mentor, related_name='mentor_datas', default=None, null=True)
    school = TextField()
    applicant = ForeignKeyField(Applicant, related_name='applicant_datas', default=None, null=True)
    detail = CharField(default=None, null=True)
    time = DateTimeField()

    @classmethod
    def get_free_slots(cls, applicant):
        return cls.select().where(cls.applicant >> None, cls.school == applicant.school).order_by(cls.time)

    def interviews(self, applicant):
        if applicant.status == "new":
            self.applicant = applicant
            self.save()
            applicant.status = "processing"
            applicant.save()

    @classmethod
    def get_interview_times(cls):
        return cls.select().join(Mentor).switch(InterviewSlot).join(Applicant)


class InterviewSlotMentor(BaseModel):
    mentor = ForeignKeyField(Mentor, related_name='mentor_interviews', default=None, null=True)
    interview = ForeignKeyField(InterviewSlot, related_name='interview_slots', default=None, null=True)

    @classmethod
    def email_to_mentors(cls):
        return InterviewSlotMentor.select().join(InterviewSlot).where(~(InterviewSlot.applicant >> None),
                                                                        InterviewSlot.detail >> None).order_by(InterviewSlot.id)


class Email_log(BaseModel):
    subject = CharField()
    message = CharField()
    type = CharField()
    date = DateTimeField()
    full_name = CharField()
    email = CharField()
