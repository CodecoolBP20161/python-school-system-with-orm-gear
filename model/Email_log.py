from model.BaseModel import BaseModel
from peewee import CharField, DateTimeField


class EmailLog(BaseModel):
    subject = CharField()
    message = CharField()
    type = CharField()
    date = DateTimeField()
    full_name = CharField()
    email = CharField()

    @classmethod
    def create_email_log(cls, subject, message, type, date, full_name, email):
        EmailLog.create(subject=subject,
                         message=message,
                         type=type,
                         date=date,
                         full_name=full_name,
                         email=email)


