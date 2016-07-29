# This script can generate example data for "City" and "InterviewSlot" models.

from models import *
from peewee import *
from main import *


class Example_data:
    applicant_dict = [{"first_name": "Zita", "last_name": "Para", "city": "Eger"},
                      {"first_name": "Elek", "last_name": "Remek", "city": "Budapest"},
                      {"first_name": "Elek", "last_name": "Beviz", "city": "Szentendre"},
                      {"first_name": "Viola", "last_name": "Ultra", "city": "Budapest"},
                      {"first_name": "Áron", "last_name": "Git", "school": "Krakow", "code": "KR2345",
                       "city": "Ostrava", "status": "accepted"}
                      ]
    city_dict = [{"applicant_city": "Szentendre", "school": "Budapest"},
                 {"applicant_city": "Eger", "school": "Miskolc"},
                 {"applicant_city": "Ostrava", "school": "Krakow"},
                 {"applicant_city": "Budapest", "school": "Budapest"}
                 ]
    mentor_dict = [{"first_name": "Tamás", "last_name": "Tompa", "school": "Budapest"},
                   {"first_name": "Dániel", "last_name": "Salamon", "school": "Budapest"},
                   {"first_name": "Miklós", "last_name": "Beöthy", "school": "Budapest"},
                   {"first_name": "Attila", "last_name": "Molnár", "school": "Miskolc"},
                   {"first_name": "Mateus", "last_name": "Ostafil", "school": "Krakow"}
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
            City.insert_many(cls.city_dict).execute()
            Mentor.insert_many(cls.mentor_dict).execute()
            InterviewSlot.insert_many(cls.interview_slot()).execute()


Example_data.insert()
