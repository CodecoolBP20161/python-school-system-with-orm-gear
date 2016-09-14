from model.BaseModel import *

class Email_log(BaseModel):
    subject = CharField()
    message = CharField()
    type = CharField()
    date = DateTimeField()
    full_name = CharField()
    email = CharField()