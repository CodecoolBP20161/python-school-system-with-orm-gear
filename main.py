from models import *
from peewee import *


class Main:

    @staticmethod
    def register():
        new_applicant = Applicant.select().where(Applicant.status == "new")
        if new_applicant:
            for applicant in new_applicant:
                applicant.update_school()

        get_applicant = Applicant.select().where(Applicant.code >> None)
        if get_applicant:
            for applicant in get_applicant:
                applicant.generate_code()

Main.register()

