from models import *
from build import *
from example_data import *
import logging
logger = logging.getLogger('peewee')
hdlr = logging.FileHandler('app.log', mode='w')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.DEBUG)
# logger.addHandler(logging.StreamHandler())

# check logs for optimize and not to use querys here only on models
# make experiments with related name and join queries
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

    @staticmethod
    def interview():
        InterviewSlot.interviews()

# Build()
# Example_data.insert()
# Main.register()
# Main.interview()

