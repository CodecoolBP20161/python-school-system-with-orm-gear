# This script can generate example data for "City" and "InterviewSlot" models.

from models import *
from peewee import *
from main import *


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
    mentor_dict = [{"first_name": "Tamás", "last_name": "Tompa", "school": "Budapest", "email": "tompat@gmail.com"},
                   {"first_name": "Dániel", "last_name": "Salamon", "school": "Budapest", "email": "salad@gmail.com"},
                   {"first_name": "Miklós", "last_name": "Beöthy", "school": "Budapest", "email": "beothym@gmail.com"},
                   {"first_name": "Attila", "last_name": "Molnár", "school": "Miskolc", "email": "molnara@gmail.com"},
                   {"first_name": "Mateus", "last_name": "Ostafil", "school": "Krakow", "email": "ostafilm@gmail.com"}
                   ]

    @staticmethod
    def interview_slot():
        interview_slot_dict = [{"mentor": Mentor.get(Mentor.first_name == "Tamás"), "time": '2016-08-28 10:00:00'},
                               {"mentor": Mentor.get(Mentor.first_name == "Tamás"), "time": '2016-08-28 11:00:00'},
                               {"mentor": Mentor.get(Mentor.first_name == "Dániel"), "time": '2016-08-29 10:00:00'},
                               {"mentor": Mentor.get(Mentor.first_name == "Dániel"), "time": '2016-08-30 11:00:00'},
                               {"mentor": Mentor.get(Mentor.first_name == "Mateus"), "time": '2016-08-27 09:00:00'},
                               {"mentor": Mentor.get(Mentor.first_name == "Attila"), "time": '2016-08-27 09:00:00'},
                               {"mentor": Mentor.get(Mentor.first_name == "Attila"), "time": '2016-08-27 10:00:00'}
                               ]
        return interview_slot_dict

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
            print('_______________________________________\n')


# Example_data.insert()
