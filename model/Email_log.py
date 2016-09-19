from model.BaseModel import BaseModel
from peewee import CharField, DateTimeField

#todo: create new method for create data for email_log after email_send

class Email_log(BaseModel):
    subject = CharField()
    message = CharField()
    type = CharField()
    date = DateTimeField()
    full_name = CharField()
    email = CharField()

    @classmethod
    def create_email_log(cls, subject, message, type, date, applicant_full_name, applicant_email):
        Email_log.create(subject=subject,
                         message=message,
                         type=type,
                         date=date,
                         full_name=applicant_full_name,
                         email=applicant_email)
