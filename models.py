from peewee import *

# Configure your database connection here
# database name = should be your username on your laptop
# database user = should be your username on your laptop
db = PostgresqlDatabase('6_teamwork_week', user='kakacsu')


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
