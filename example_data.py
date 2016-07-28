# This script can generate example data for "City" and "InterviewSlot" models.

from models import *
from peewee import *
from main import *

applicant_dict = [{"first_name": "Zita", "last_name": "Para", "city": "Eger"},
                  {"first_name": "Elek", "last_name": "Remek", "city": "Budapest"},
                  {"first_name": "Elek", "last_name": "Beviz", "city": "Szentendre"},
                  {"first_name": "Viola", "last_name": "Ultra", "city": "Budapest"},
                  {"first_name": "Áron", "last_name": "Git", "school": "Krakow", "code": "KR1234",
                   "city": "Ostrava", "status": "accepted"}
                  ]

with db.atomic():
    Applicant.insert_many(applicant_dict).execute()

city_dict = [{"applicant_city": "Szentendre", "school": "Budapest"},
             {"applicant_city": "Eger", "school": "Miskolc"},
             {"applicant_city": "Ostrava", "school": "Krakow"},
             {"applicant_city": "Budapest", "school": "Budapest"}
             ]

with db.atomic():
    City.insert_many(city_dict).execute()

mentor_dict = [{"first_name": "Tamás", "last_name": "Tompa", "school": "Budapest"},
               {"first_name": "Dániel", "last_name": "Salamon", "school": "Budapest"},
               {"first_name": "Miklós", "last_name": "Beöthy", "school": "Budapest"},
               {"first_name": "Attila", "last_name": "Molnár", "school": "Miskolc"},
               {"first_name": "Mateus", "last_name": "Ostafil", "school": "Krakow"}
               ]

with db.atomic():
    Mentor.insert_many(mentor_dict).execute()

mentor1 = Mentor.get(Mentor.first_name == "Tamás")
mentor2 = Mentor.get(Mentor.first_name == "Dániel")
mentor3 = Mentor.get(Mentor.first_name == "Attila")
mentor4 = Mentor.get(Mentor.first_name == "Mateus")

interview_slot_dict = [{"mentor": mentor1, "time": '2016-08-28 10:00:00'},
                       {"mentor": mentor1, "time": '2016-08-28 11:00:00'},
                       {"mentor": mentor2, "time": '2016-08-29 10:00:00'},
                       {"mentor": mentor2, "time": '2016-08-30 11:00:00'},
                       {"mentor": mentor4, "time": '2016-08-27 09:00:00'},
                       {"mentor": mentor3, "time": '2016-08-27 09:00:00'},
                       {"mentor": mentor3, "time": '2016-08-27 10:00:00'}
                       ]

with db.atomic():
    InterviewSlot.insert_many(interview_slot_dict).execute()
