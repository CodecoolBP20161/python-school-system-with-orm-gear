from model.Applicant import Applicant
from model.BaseModel import db
from model.City import City
from model.Email_log import EmailLog
from model.InterviewSlot import InterviewSlot
from model.InterviewSlotMentor import InterviewSlotMentor
from model.Mentor import Mentor
from model.Person import Person


class Build:
    @staticmethod
    def connect():
        db.connect()
        print('Connected to database')

    @staticmethod
    def drop():
        db.drop_tables([Person, Applicant, City, Mentor, InterviewSlot, InterviewSlotMentor, EmailLog], safe=True)
        print('Deleted tables')

    @staticmethod
    def create():
        db.create_tables([Person, Applicant, City, Mentor, InterviewSlot, InterviewSlotMentor, EmailLog], safe=True)
        print("Created tables\n")

# Build()
