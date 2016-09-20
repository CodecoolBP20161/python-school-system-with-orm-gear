from datetime import *

from model.Applicant import Applicant
from model.Email_log import Email_log
from model.InterviewSlot import InterviewSlot
from model.InterviewSlotMentor import InterviewSlotMentor
from model.Mentor import Mentor
from model.Send_email.emails import *
from model.Send_email.message import *


class Main:
    @classmethod
    def register(cls):

        Applicant.update_school()
        Applicant.set_code()

        print('_______________________________________\n')
        print("Sending out e-mails to new applicants.\n")
        Applicant.send_mail()
        InterviewSlot.interviews()
        print('_______________________________________\n')
        print('Sending out e-mails to applicants who were assigned to an interview.\n')
        cls.send_email_interview()
        print('_______________________________________\n')
        print('Sending out e-mails to mentors who were assigned to an interview.\n')
        InterviewSlotMentor.send_email_interview_mentors()


    @classmethod
    def send_email_interview(cls):
        email_data = dict()
        # todo: refactor email sender get_user_email_data in email sender creat some facade pattern to it, and email.send method refactor as instance method
        for i, applicant in enumerate(Applicant.select(Applicant, InterviewSlot, InterviewSlotMentor, Mentor).join(
                InterviewSlot).join(InterviewSlotMentor).join(Mentor).where(Applicant.status == "processing")):

            if i % 2:
                message_dict = Message(applicant.first_name,
                                       applicant.interviewslot.time,
                                       applicant.interviewslot.interviewslotmentor.mentor.full_name,
                                       email_data["mentor1_full_name"])
                message_dict = message_dict.applicant_interview()
                sent_email = Email(applicant.email, **message_dict)
                sent_email.send_mail()
                Email_log.create_email_log(message_dict['subject'], message_dict['body'], "applicant's interview",
                                           datetime.utcnow(), applicant.full_name, applicant.email)

            else:
                email_data.update({"mentor1_full_name": applicant.interviewslot.interviewslotmentor.mentor.full_name})





            # todo: refcator interview method handle in one place

    # @classmethod
    # def interview(cls):
    #     for new in Applicant.filter("status", "new"):
    #         for i in InterviewSlot.get_free_slots(new):
    #             i.interviews(new)
    # InterviewSlot.interviews()
    # print('_______________________________________\n')
    # print('Sending out e-mails to applicants who were assigned to an interview.\n')
    # # Main.send_email_interview()
    # print('_______________________________________\n')
    # print('Sending out e-mails to mentors who were assigned to an interview.\n')
    # InterviewSlotMentor.send_email_interview_mentors()


# Build.connect()
# Build.drop()
# Build.create()
# Example_data.insert()
# Main.get_user_email_data()
# Main.register()
# Main.interview()
print("Please start with app.py")
