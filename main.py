
from initialize.example_data import Example_data
from initialize.build import Build
from model.Applicant import Applicant
from model.InterviewSlot import InterviewSlot
from model.InterviewSlotMentor import InterviewSlotMentor
from app import app


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
        # cls.send_email_interview()
        Applicant.send_app_int()
        print('_______________________________________\n')
        print('Sending out e-mails to mentors who were assigned to an interview.\n')
        InterviewSlotMentor.send_email_interview_mentors()


if __name__ == '__main__':
    # Build.drop()
    Build.create()
    applicant  =Applicant.select()
    if len(applicant) == 0:
        Example_data.insert()
    Main.register()
    # app.run()
    app.run(debug=True)
