from models import *
from peewee import *

new_applicant = Applicant.select().where(Applicant.status == "new")
for applicant in new_applicant:
    applicant.update_school()
# query = Applicant.update(school="new shcool").where(Applicant.id == 1)
# for i in new_applicant:
#     query = i.update_school("method")
#     query.execute()
# # new_applicant.update_school("new school")
# city_model = City.select(City.applicant_city)
# city_model = [city.applicant_city for city in city_model]
#
# for member in new_applicant:
#     if member.city in city_model:
#         school_get = Applicant.select(Applicant, City).join(City, on=Applicant.city == City.applicant_city).where(
#             member.city == City.applicant_city).get()
#         member.update_school(school_get.city.school)
#         # update_query = member.update(Applicant.school == school_get.city.school)
#         # update_query.execute()
#         print(member.city)
#         print(school_get.city.school)
