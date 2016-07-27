from peewee import *
import random

# Configure your database connection here
# database name = should be your username on your laptop
# database user = should be your username on your laptop

def read_from_txt():
    import os.path
    scriptpath = os.path.dirname(__file__)
    filename = os.path.join(scriptpath, 'user.txt')
    with open(filename) as f:
        data = f.read()
        data = data.strip("\n")
        return data

db = PostgresqlDatabase('6_teamwork_week', user=read_from_txt())



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
    code = CharField(default=None, null=True)
    city = TextField()
    status = CharField(default='new')

    def update_school(self):
        school_get = City.get(City.applicant_city == self.city).school
        update_query = Applicant.update(school=school_get).where(Applicant.id == self.id)
        update_query.execute()

    def generate_code(self):
        # get_codes = Applicant.select().where(~(Applicant.code >> None)).code
        new_code = "".join([self.first_name[:2], self.last_name[:2], str(random.randint(100, 1000)), self.city[:2].upper()])
        update_query = Applicant.update(code=new_code, status="processing").where(Applicant.id == self.id)
        update_query.execute()



