from peewee import ForeignKeyField, TextField, CharField, DateTimeField
from model.BaseModel import BaseModel
from model.Applicant import Applicant
from model.Mentor import Mentor
# from controll_admin import *


class InterviewSlot(BaseModel):
    mentor = ForeignKeyField(Mentor, related_name='mentor_datas', default=None, null=True)
    school = TextField()
    applicant = ForeignKeyField(Applicant, related_name='applicant_datas', default=None, null=True)
    detail = CharField(default=None, null=True)
    time = DateTimeField()

    @classmethod
    def get_free_slots(cls, applicant):
        return cls.select().where(cls.applicant >> None, cls.school == applicant.school).order_by(cls.time)

#todo: refactor get interviews method
    def interviews(self, applicant):
        if applicant.status == "new":
            self.applicant = applicant
            self.save()
            applicant.status = "processing"
            applicant.save()

    @classmethod
    def get_interview_times(cls):
        return cls.select().join(Mentor).switch(InterviewSlot).join(Applicant)

