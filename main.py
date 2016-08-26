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

    @classmethod
    def register(cls):
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
        print('_______________________________________\n')
        print("Sending out e-mails to new applicants.\n")
        cls.send_mail()

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
        for applicant in Applicant.get_interviewed_applicant():
            for applic in applicant.applicant_datas:
                if applic.detail is None:
                    mentors = applicant.get_mentors_for_interview("mentors")
                    message_dict = Message.applicant_interview(applicant.first_name, applicant.get_mentors_for_interview("time"),
                                                               *mentors)
                    Email.send_email(applicant.email, **cls.user_data, **message_dict)

    @classmethod
    def send_email_interview_mentors(cls):
        for interview in InterviewSlotMentor.email_to_mentors():
            message_dict = Message.mentor_interview(interview.mentor.first_name, interview.interview.time,
                                                    interview.interview.applicant.first_name, interview.interview.applicant.last_name)

            Email.send_email(interview.mentor.email, **cls.user_data, **message_dict)
            interview.interview.detail = "email sent"
            interview.interview.save()


    @classmethod
    def interview(cls):
        for new in Applicant.new_applicant():
            for i in InterviewSlot.get_free_slots(new):
                i.interviews(new)
        print('_______________________________________\n')
        print('Sending out e-mails to applicants who were assigned to an interview.\n')
        cls.send_email_interview()
        print('_______________________________________\n')
        print('Sending out e-mails to mentors who were assigned to an interview.\n')
        cls.send_email_interview_mentors()




# Build()
# Example_data.insert()
# Main.register()
# Main.interview()
print("Please start with menu.py")
