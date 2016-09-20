from peewee import ForeignKeyField, TextField, CharField, DateTimeField
from model.BaseModel import BaseModel
from model.Applicant import Applicant
from model.Mentor import Mentor


class InterviewSlot(BaseModel):
    mentor = ForeignKeyField(Mentor, related_name='mentor_datas', default=None, null=True)
    school = TextField()
    applicant = ForeignKeyField(Applicant, related_name='applicant_datas', default=None, null=True)
    detail = CharField(default=None, null=True)
    time = DateTimeField()

    @classmethod
    def get_free_slots(cls, applicant):
        return cls.select().where(cls.applicant >> None, cls.school == applicant.school).order_by(cls.time)

    @classmethod
    def interviews(cls):
        for new in Applicant.filter("status", "new"):
            for applicant in cls.get_free_slots(new):
                if new.status == "new":
                    applicant.applicant = new
                    applicant.save()
                    new.status = "processing"
                    new.save()







