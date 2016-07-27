from peewee import *

# Configure your database connection here
# database name = should be your username on your laptop
# database user = should be your username on your laptop
db = PostgresqlDatabase('kakacsu', user='kakacsu')


class BaseModel(Model):
    """A base model that will use our Postgresql database"""
    class Meta:
        database = db


class Person(BaseModel):
        first_name = CharField()
        last_name = CharField()
        school = CharField()


class Applicant(Person):
        code = CharField()
        city = TextField()
        status = TextField()


class City(BaseModel):
        applicant_city = TextField()
        school = TextField()

        class Meta:
            database = db
