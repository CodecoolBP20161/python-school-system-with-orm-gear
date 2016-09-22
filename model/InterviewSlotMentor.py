from model.BaseModel import BaseModel
from model.Mentor import Mentor
from model.InterviewSlot import InterviewSlot
from peewee import ForeignKeyField
from model.Email_log import EmailLog
from model.Send_email.emails import Email
from model.Send_email.message import Message
from datetime import *


class InterviewSlotMentor(BaseModel):
    mentor = ForeignKeyField(Mentor, related_name='interview_slotmentors', default=None, null=True)
    interview = ForeignKeyField(InterviewSlot, related_name='interview_slotmentors', default=None, null=True)

    @classmethod
    def email_to_mentors(cls):
        return InterviewSlotMentor.select().join(InterviewSlot).where(~(InterviewSlot.applicant >> None),
                                                                      InterviewSlot.detail >> None).order_by(
            InterviewSlot.id)

    def update_send_email(self, status):
        self.interview.detail = status
        self.interview.save()

    @classmethod
    def send_email_interview_mentors(cls):
        for interview in cls.email_to_mentors():
            message_dict = Message(interview.mentor.first_name,
                                   interview.interview.time,
                                   interview.interview.applicant.full_name)
            message_dict = message_dict.mentor_interview()

            log = [message_dict['subject'], message_dict['body'], "mentors's interview",
                   datetime.utcnow(), interview.mentor.full_name, interview.mentor.email]
            sent_email = Email(interview.mentor.email, **message_dict)
            sent_email.send_mail(log)
            interview.update_send_email("email sent")
