# This script can generate example data for "City" and "InterviewSlot" models.

from models import *
from peewee import *

city_attribute = ["applicant_city", "school_city"]
applicant_attribute = ["first_name", "last_name", "school", "code", "city",  "status"]


city_rows = [["Eger", "Miskolc"],
             ["Balassagyarmat", "Budapest"],
             ["Vac", "Budapest"],
             ["Budapest", "Budapest"],
             ["Ostrava", "Krakow"]
             ]

applicant_rows = [["Janos", "Kiss", None, None, "Eger", "new"],
                  ["Anna", "Nagy", None, None, "Vac",  "new"],
                  ["Joci", "Galambos", None, None, "Budapest", "new"],
                  ["Ágnes", "Jakabos", None, None, "Balassagyarmat", "new"]
                  ]

city_dict = []
applicant_dict = []

for i in len(city_rows):
    city_dict.append(dict(zip(city_attribute, city_rows[i])))

for j in len(applicant_dict):
    applicant_dict.append(dict(zip(applicant_attribute, applicant_rows[i])))


# insert in a fast way
with db.atomic():
    City.insert_many(city_dict).execute()
    Applicant_dict.insert_many(applicant_dict).execute()
