from models import *
from build import *
from example_data import *
# import logging
# logger = logging.getLogger('peewee')
# logger.setLevel(logging.DEBUG)
# logger.addHandler(logging.StreamHandler())


class Main:

    @staticmethod
    def register():
        new_applicant = Applicant.new_applicant()
        if new_applicant:
            for applicant in new_applicant:
                applicant.update_school()

        get_applicant = Applicant.select().where(Applicant.code >> None)
        if get_applicant:
            for applicant in get_applicant:
                applicant.generate_code()
                print(applicant.code, applicant.first_name, applicant.last_name, applicant.city, applicant.school, applicant.status)

    @staticmethod
    def interview():
        for new in Applicant.new_applicant():
            for i in InterviewSlot.get_free_slots():
                i.interviews(new)



# Build()
# Example_data.insert()
# Main.register()
# Main.interview()
