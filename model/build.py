# This script can create the database tables based on your models

from model.Applicant import Applicant
from model.Person import Person
from model.City import City
from model.Mentor import Mentor
from model.InterviewSlot import InterviewSlot
from model.InterviewSlotMentor import InterviewSlotMentor
from model.Email_log import Email_log
from model.BaseModel import *


class Build:
    # db.connect()
    # List the tables here what you want to create...
    # db.drop_tables([Person, Applicant, City, Mentor, InterviewSlot, safe=True)
    # db.create_tables([Person, Applicant, City, Mentor, InterviewSlot], safe=True)

    @staticmethod
    def connect():
        db.connect()
        print('Connected to database')

    @staticmethod
    def drop():
        db.drop_tables([Person, Applicant, City, Mentor, InterviewSlot, InterviewSlotMentor, Email_log], safe=True)
        print('Deleted tables')

    @staticmethod
    def create():
        db.create_tables([Person, Applicant, City, Mentor, InterviewSlot, InterviewSlotMentor, Email_log], safe=True)
        print("Created tables\n")

# Build()
