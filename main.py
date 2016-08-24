from models import *
from build import *
from example_data import *
from message import *
from user import *
from emails import *

# import logging
# logger = logging.getLogger('peewee')
# hdlr = logging.FileHandler('app.log', mode='w')
# formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
# hdlr.setFormatter(formatter)
# logger.addHandler(hdlr)
# logger.setLevel(logging.DEBUG)


# logger.addHandler(logging.StreamHandler())

# check logs for optimize and not to use querys here only on models
# make experiments with related name and join queries



class Main:

    user_data = {}

    @staticmethod
    def register():
        new_applicant = Applicant.new_applicant()
        if new_applicant:
            for applicant in new_applicant:
                applicant.update_school()

        get_applicant = Applicant.select().where(Applicant.code >> None)
        if get_applicant:
            for applicant in get_applicant:
                applicant.generate_code()
                print(applicant.code, applicant.first_name, applicant.last_name, applicant.city, applicant.school,
                      applicant.status, applicant.email)

    @classmethod
    def get_user_email_data(cls):
        cls.user_data = User.create_file()

    @classmethod
    def send_mail(cls):
        for applicant in Applicant.get_assigned_applicants():
            message_dict = Message.new_applicant(applicant.first_name, applicant.code, applicant.school)
            Email.send_email(applicant.email, **cls.user_data, **message_dict)

    @classmethod
    def send_email_interview(cls):
        for interview in InterviewSlot.get_interview_times():
            message_dict = Message.applicant_interview(interview.applicant.first_name, interview.time,
                                                       interview.mentor.first_name, interview.mentor.last_name)
            # message_dict = {"subject": "proba", "body": "message"}

            Email.send_email(interview.applicant.email, **cls.user_data, **message_dict)

    @classmethod
    def send_email_interview_mentors(cls):
        for interview in InterviewSlot.get_interview_times():
            message_dict = Message.mentor_interview(interview.mentor.first_name, interview.time,
                                                    interview.applicant.first_name, interview.applicant.last_name)
            # message_dict = {"subject": "proba", "body": "message"}
            Email.send_email(interview.mentor.email, **cls.user_data, **message_dict)

    @staticmethod
    def interview():
        for new in Applicant.new_applicant():
            for i in InterviewSlot.get_free_slots():
                i.interviews(new)

# Build()
# Example_data.insert()
# Main.register()
# Main.interview()
