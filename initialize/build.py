# This script can create the database tables based on your models

from psycopg2 import connect
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from initialize.Database_info import Database_info
from model.Applicant import Applicant
from model.BaseModel import db
from model.City import City
from model.Email_log import Email_log
from model.InterviewSlot import InterviewSlot
from model.InterviewSlotMentor import InterviewSlotMentor
from model.Mentor import Mentor
from model.Person import Person


class Build:

#todo: create database if it is not exist try with local password why it is not working????
    @staticmethod
    def connect_db():
        try:
            con = connect(user=Database_info.db_user_name(), host='localhost', password=Database_info.db_password(),
                          port=5432)

            con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cur = con.cursor()
            cur.execute('CREATE DATABASE ' + Database_info.db_name())
            cur.close()
            con.close()
        except:
            print("Database already exist")

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
