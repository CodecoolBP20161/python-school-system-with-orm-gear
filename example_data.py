# This script can generate example data for "City" and "InterviewSlot" models.

from models import *
from peewee import *

applicant_dict = [{"first_name": "Janos", "last_name": "Kiss", "city": "Eger"},
                  {"first_name": "Ági", "last_name": "Kincses", "city": "Budapest"},
                  {"first_name": "Görbe", "last_name": "Barna", "city": "Szentendre"},
                  {"first_name": "Virág", "last_name": "Ibolya", "city": "Budapest"}
                  ]

city_dict = [{"applicant_city": "Szentendre", "school": "Budapest"},
             {"applicant_city": "Eger", "school": "Miskolc"},
             {"applicant_city": "Ostrava", "school": "Krakow"},
             {"applicant_city": "Budapest", "school": "Budapest"}
             ]
student = Applicant.create(first_name="Pista", last_name="Előd", school="Krakow", code="KR1234", city="Ostrava",
                           status="accpeted")

# insert in a fast way
with db.atomic():
    City.insert_many(city_dict).execute()
    Applicant.insert_many(applicant_dict).execute()
