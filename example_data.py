# This script can generate example data for "City" and "InterviewSlot" models.

from models import *
from peewee import *
from main import *

applicant_dict = [{"first_name": "Janos", "last_name": "Kiss", "city": "Eger"},
                  {"first_name": "Ági", "last_name": "Kincses", "city": "Budapest"},
                  {"first_name": "Görbe", "last_name": "Barna", "city": "Szentendre"},
                  {"first_name": "Virág", "last_name": "Ibolya", "city": "Budapest"}
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
student = Applicant.create(first_name="Pista", last_name="Előd", school="Krakow", code="KR1234", city="Ostrava",
                           status="accpeted")

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

# insert in a fast way
with db.atomic():
    InterviewSlot.insert_many(interview_slot_dict).execute()
