from model.BaseModel import BaseModel
from model.Mentor import Mentor
from model.InterviewSlot import InterviewSlot
from peewee import ForeignKeyField
# from controll_admin import *


class InterviewSlotMentor(BaseModel):
    mentor = ForeignKeyField(Mentor, related_name='interview_slotmentors', default=None, null=True)
    interview = ForeignKeyField(InterviewSlot, related_name='interview_slotmentors', default=None, null=True)

    @classmethod
    def email_to_mentors(cls):
        return InterviewSlotMentor.select().join(InterviewSlot).where(~(InterviewSlot.applicant >> None),
                                                                      InterviewSlot.detail >> None).order_by(
            InterviewSlot.id)