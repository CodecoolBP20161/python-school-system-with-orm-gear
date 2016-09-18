from peewee import *
import random
from read_from_text import *
from datetime import *
from Database_info import Database_info

# db = PostgresqlDatabase(Database_info.db_name(), user=Database_info.db_user_name())
db = PostgresqlDatabase(Database_info.db_name(),
                        **{'user': Database_info.db_user_name(), 'host': 'localhost', 'port': 5432,
                           'password': '753951'})


class BaseModel(Model):
    """A base model that will use our Postgresql database"""

    class Meta:
        database = db

    @classmethod
    def filter(cls, attribute, filter):
        try:
            result = cls.select().where(getattr(cls, attribute) == filter)
        except AttributeError:
            result = None
            print(
                "wrong attribute your {0} select().where({0}.{1} == {2}), query is bad".format(cls, attribute, filter))
        return result

    @classmethod
    def option_groups(cls, groups):
        result = []
        for group in groups:
            attribute = getattr(cls, group)
            result.append(cls.select(attribute).group_by(attribute))
        return result


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

    @classmethod
    def update_school(cls):
        new_applicant = cls.filter("status", "new")
        if new_applicant:
            for applicant in new_applicant:
                school_get = City.get(City.applicant_city == applicant.city).school
                applicant.school = school_get
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

    @classmethod
    def get_interviewed_applicant(cls):
        return cls.select().where(cls.status == "processing")

    def get_mentors_for_interview(self):
        mentors = []

        # for mentor in InterviewSlotMentor.select():
        #     if applicant.id == mentor.interview.id:
        #         mentors.append(mentor.mentor.first_name)
        #         mentors.append(mentor.mentor.last_name)
        #         # print(mentor.mentor.first_name, mentor.mentor.last_name)
        #
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

    # @classmethod
    # def mentors_for_applicant(cls, first_name, last_name):
    #     return cls.select(Applicant, InterviewSlot, InterviewSlotMentor, Mentor).join(
    #         InterviewSlot).join(
    #         InterviewSlotMentor).join(Mentor).where(Mentor.first_name.contains(first_name),
    #                                                 Mentor.last_name.contains(last_name))


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

    # @classmethod
    # def inter_views(cls):
    #     for new_applicant in Applicant.filter("status", "new"):
    #         for interview in cls.get_free_slots(new_applicant):
    #             interview.applicant = new_applicant
    #             interview.save()
    #             new_applicant.status = "processing"
    #             new_applicant.save()

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
                                                                      InterviewSlot.detail >> None).order_by(
            InterviewSlot.id)


class Email_log(BaseModel):
    subject = CharField()
    message = CharField()
    type = CharField()
    date = DateTimeField()
    full_name = CharField()
    email = CharField()
