from peewee import *
import random
from read_from_text import *

db = PostgresqlDatabase('6_teamwork_week', user=Read_from_text.connect_data())
# db = PostgresqlDatabase('6_teamwork_week',
#                           **{'user': Read_from_text.connect_data(), 'host': 'localhost', 'port': 5432, 'password': '753951'})


class BaseModel(Model):
    """A base model that will use our Postgresql database"""

    class Meta:
        database = db


class Person(BaseModel):
    first_name = CharField()
    last_name = CharField()
    school = CharField(default='', null=True)
    email = CharField()


class City(BaseModel):
    applicant_city = TextField()
    school = TextField()


class Applicant(Person):
    code = CharField(default=None, null=True, unique=True)
    city = TextField()
    status = CharField(default='new')

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


class Mentor(Person):
    pass


class InterviewSlot(BaseModel):
    mentor = ForeignKeyField(Mentor, related_name='mentor_datas', default=None, null=True)
    mentor2 = ForeignKeyField(Mentor, related_name='mentor2_datas', default=None, null=True)
    school = TextField()
    applicant = ForeignKeyField(Applicant, related_name='applicant_datas', default=None, null=True)
    detail = CharField(default=None, null=True)
    time = DateTimeField()

    @classmethod
    def get_free_slots(cls, applicant):
        return cls.select().where(cls.mentor >> None, cls.applicant >> None, cls.school == applicant.school).order_by(cls.time)

    def interviews(self, applicant):
        if applicant.status == "new":
            self.applicant = applicant
            self.save()
            mentor1 = Mentor.select().where(self.school == Mentor.school)
            self.mentor = random.choice(mentor1)
            self.save()
            for mentor in mentor1:
                if mentor != self.mentor:
                    self.mentor2 = mentor
                    self.save()

            applicant.status = "processing"
            applicant.save()



    @classmethod
    def get_interview_times(cls):
        return cls.select().join(Mentor).switch(InterviewSlot).join(Applicant)


















#
