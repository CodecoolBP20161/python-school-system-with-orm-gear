from app import app
from initialize.build import Build
from initialize.example_data import ExampleData
from model.Applicant import Applicant
from model.InterviewSlot import InterviewSlot
from model.InterviewSlotMentor import InterviewSlotMentor


class Main:

    @staticmethod
    def register():
        Applicant.update_school()
        Applicant.set_code()
        print('_______________________________________\n')
        print("Sending out e-mails to new applicants.\n")
        Applicant.send_mail_for_new_applicant()
        InterviewSlot.interviews()
        print('_______________________________________\n')
        print('Sending out e-mails to applicants who were assigned to an interview.\n')
        # cls.send_email_interview()
        Applicant.send_applicant_interview_email()
        print('_______________________________________\n')
        print('Sending out e-mails to mentors who were assigned to an interview.\n')
        InterviewSlotMentor.send_email_interview_mentors()

if __name__ == '__main__':
    # Build.drop()
    Build.create()
    applicant = Applicant.select()
    if len(applicant) == 0:
        ExampleData.insert()
    Main.register()
    # app.run()
    app.run(debug=True)
