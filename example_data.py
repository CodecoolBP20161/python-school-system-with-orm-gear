# This script can generate example data for "City" and "InterviewSlot" models.

from models import *
from peewee import *
from main import *
import random


class Example_data:
    applicant_dict = [{"first_name": "Zita", "last_name": "Para", "email": "girhes.cc.2016@gmail.com", "city": "Eger"},
                      {"first_name": "Elek", "last_name": "Remek", "email": "remekelek@gmail.com", "city": "Budapest"},
                      {"first_name": "Elek", "last_name": "Beviz", "email": "bevize@gmail.com", "city": "Szentendre"},
                      {"first_name": "Viola", "last_name": "Ultra", "email": "ultrav@gmail.com", "city": "Budapest"},
                      {"first_name": "Áron", "last_name": "Git", "school": "Krakow",
                       "email": "gitaron@gmail.com", "code": "KR2345", "city": "Ostrava", "status": "accepted"}
                      ]
    city_dict = [{"applicant_city": "Szentendre", "school": "Budapest"},
                 {"applicant_city": "Eger", "school": "Miskolc"},
                 {"applicant_city": "Ostrava", "school": "Krakow"},
                 {"applicant_city": "Budapest", "school": "Budapest"}
                 ]
    mentor_dict = [
        {"first_name": "Tamás", "last_name": "Tompa", "school": "Budapest", "email": "girhes.cc.2016@gmail.com"},
        {"first_name": "Dániel", "last_name": "Salamon", "school": "Budapest", "email": "girhes.cc.2016@gmail.com"},
        {"first_name": "Miklós", "last_name": "Beöthy", "school": "Budapest", "email": "girhes.cc.2016@gmail.com"},
        {"first_name": "Attila", "last_name": "Molnár", "school": "Miskolc", "email": "girhes.cc.2016@gmail.com"},
        {"first_name": "Mateus", "last_name": "Ostafil", "school": "Krakow", "email": "girhes.cc.2016@gmail.com"},
        {"first_name": "Károly", "last_name": "Nagy", "school": "Miskolc",
         "email": "girhes.cc.2016@gmail.com"},
        {"first_name": "James", "last_name": "Brown", "school": "Krakow",
         "email": "girhes.cc.2016@gmail.com"}
        ]

    @staticmethod
    def interview_slot():
        interview_slot_dict = [{"school": "Budapest", "time": '2016-08-28 10:00:00'},
                               {"school": "Budapest", "time": '2016-08-28 11:00:00'},
                               {"school": "Budapest", "time": '2016-08-27 10:00:00'},
                               {"school": "Budapest", "time": '2016-08-27 11:00:00'},
                               {"school": "Budapest", "time": '2016-08-29 10:00:00'},
                               {"school": "Budapest", "time": '2016-08-26 11:00:00'},
                               {"school": "Krakow", "time": '2016-08-27 09:00:00'},
                               {"school": "Krakow", "time": '2016-08-28 09:00:00'},
                               {"school": "Krakow", "time": '2016-08-29 09:00:00'},
                               {"school": "Miskolc", "time": '2016-08-27 09:00:00'},
                               {"school": "Miskolc", "time": '2016-08-27 10:00:00'},
                               {"school": "Miskolc", "time": '2016-08-28 09:00:00'},
                               {"school": "Miskolc", "time": '2016-08-28 10:00:00'},
                               {"school": "Krakow", "time": '2016-08-28 10:00:00'}
                               ]
        return interview_slot_dict

    @staticmethod
    def interview_slot_mentor():
        interview = InterviewSlot.select().order_by(InterviewSlot.time)
        interview_list = []
        for interviews in interview:
            mentors = Mentor.select().where(interviews.school == Mentor.school)

            mentors1 = random.choice(mentors)
            for i in range(10):
                mentors2 = random.choice(mentors)
                if mentors2.first_name != mentors1.first_name:
                    break

            interview_list.append({"mentor": mentors1, "interview": interviews})
            interview_list.append({"mentor": mentors2, "interview": interviews})

        return interview_list


    @classmethod
    def insert(cls):
        with db.atomic():
            Applicant.insert_many(cls.applicant_dict).execute()
            print("Applicants created")
            City.insert_many(cls.city_dict).execute()
            print("Cities created")
            Mentor.insert_many(cls.mentor_dict).execute()
            print("Mentors created")
            InterviewSlot.insert_many(cls.interview_slot()).execute()
            print("Interview slots created")
            InterviewSlotMentor.insert_many(cls.interview_slot_mentor()).execute()
            print('_______________________________________\n')
        cls.interview_slot_mentor()

# Example_data.insert()
