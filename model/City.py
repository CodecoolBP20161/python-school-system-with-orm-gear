from model.BaseModel import BaseModel
from peewee import TextField


class City(BaseModel):
    applicant_city = TextField()
    school = TextField()
