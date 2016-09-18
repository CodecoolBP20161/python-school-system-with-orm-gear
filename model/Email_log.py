from model.BaseModel import BaseModel
from peewee import CharField, DateTimeField


class Email_log(BaseModel):
    subject = CharField()
    message = CharField()
    type = CharField()
    date = DateTimeField()
    full_name = CharField()
    email = CharField()