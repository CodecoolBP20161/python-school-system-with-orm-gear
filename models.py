from peewee import *

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
        school = CharField(default=' ', null=True)


class Applicant(Person):
        code = CharField(default=' ', null=True)
        city = TextField()
        status = default = 0


class City(BaseModel):
        applicant_city = TextField()
        school = TextField()
