from models import *
from build import *
from example_data import *
from message import *
from user import *
from emails import *
# import logging
# logger = logging.getLogger('peewee')
# logger.setLevel(logging.DEBUG)
# logger.addHandler(logging.StreamHandler())


class Main:

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

    @staticmethod
    def send_mail():
        email_to_applicants = Applicant.get_assigned_applicants()
        user_data = User.create_file()
        for applicant in email_to_applicants:
            message_dict = Message.new_applicant(applicant.first_name, applicant.code, applicant.school)
            Email.send_email(applicant.email, **user_data, **message_dict)

    @staticmethod
    def send_email_interview():
        interviews = InterviewSlot.get_interview_times()
        user_data = User.create_file()
        for interview in interviews:
            message_dict = Message.applicant_interview(interview.applicant.first_name, interview.time,
                                                       interview.mentor.first_name, interview.mentor.last_name)
            Email.send_email(interview.applicant.email, **user_data, **message_dict)

    @staticmethod
    def interview():
        for new in Applicant.new_applicant():
            for i in InterviewSlot.get_free_slots():
                i.interviews(new)



# Build()
# Example_data.insert()
# Main.register()
# Main.interview()
