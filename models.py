from peewee import *
import random
from read_from_text import *

# db = PostgresqlDatabase('6_teamwork_week', user=Read_from_text.connect_data())
db = PostgresqlDatabase('6_teamwork_week',
                        **{'user': Read_from_text.connect_data(), 'host': 'localhost', 'port': 5432, 'password': '753951'})


class BaseModel(Model):
    """A base model that will use our Postgresql database"""

    class Meta:
        database = db


class Person(BaseModel):
    first_name = CharField()
    last_name = CharField()
    school = CharField(default='', null=True)


class City(BaseModel):
    applicant_city = TextField()
    school = TextField()


class Applicant(Person):
    code = CharField(default=None, null=True, unique=True)
    city = TextField()
    status = CharField(default='new')

    @classmethod
    def new_applicant(cls):
        return Applicant.select().where(Applicant.status == "new")

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


class Mentor(Person):
    pass


class InterviewSlot(BaseModel):
    mentor = ForeignKeyField(Mentor, related_name='mentor_datas')
    applicant = ForeignKeyField(Applicant, related_name='applicant_datas', default=None, null=True)
    detail = CharField(default=None, null=True)
    time = DateTimeField()

    @classmethod
    def get_free_slots(cls):
        return InterviewSlot.select().where(cls.applicant >> None).order_by(cls.time)

    def interviews(self, applicant):
        if applicant.school == self.mentor.school and applicant.status == "new":
            self.applicant = applicant
            self.save()
            applicant.status = "processing"
            applicant.save()

