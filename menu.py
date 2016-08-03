from build import *
from example_data import *
from main import *
from models import *
from peewee import *


class Menu():


# too much information in one method let's separate it, and use only print functions move queries to models or main.py
    @classmethod
    def select_option(cls):
        available_choices = ['(1) Generate New Database', '(2) Display Applicants', '(3) Application Details', '(4) Interview Details', '(5) Update', '(0) Exit']
        menu_choice = None
        while menu_choice != '0':
            print('_______________________________________\n')
            for i in available_choices:
                print(i)
            menu_choice = input('\nPlease select a number: ')
            # print('_______________________________________\n')
            if menu_choice == '1':
                print('_______________________________________\n')
                Build.connect()
                Build.drop()
                Build.create()
                Example_data.insert()
                Main.register()
                Main.interview()
            if menu_choice == '2':
                print('_______________________________________\n')
                applicants = Applicant.select()
                for applicant in applicants:
                    print(applicant.code, applicant.first_name, applicant.last_name, applicant.city, applicant.school, applicant.status)
                cls.proba()

            if menu_choice == '3':
                application_code = input('Please enter your Application Code: ')
                try:
                    existed_applicant = Applicant.get(Applicant.code == application_code)
                    print('_______________________________________\n')
                    print('School: {0}\nStatus: {1}'.format(existed_applicant.school, existed_applicant.status))
                except Applicant.DoesNotExist:
                    print("Unavaible Application Code")
            if menu_choice == '4':
                application_code = input('Please enter your Application Code: ')
                try:
                    existed_applicant = Applicant.get(Applicant.code == application_code)
                    interview = InterviewSlot.get(InterviewSlot.applicant == existed_applicant)
                    print('_______________________________________\n')
                    print('Date: {0}\nSchool: {1}\nMentor: {2} {3}'.format(interview.time, existed_applicant.school, interview.mentor.first_name, interview.mentor.last_name))
                except Applicant.DoesNotExist:
                    print("Unavaible Application Code")
            if menu_choice == '5':
                print('_______________________________________\n')
                Main.register()
                Main.interview()

    @staticmethod
    def proba():
        mentor = Mentor.get(Mentor.first_name == "Tamás")
        app = Applicant.select(Applicant, Mentor).join(Mentor, on=Applicant.school == Mentor.school).order_by()
        apps = Applicant.select().where(Applicant.status == "in progress")
        interview = InterviewSlot.get(InterviewSlot.mentor == mentor)
        join = InterviewSlot.select(InterviewSlot, Applicant).join(Applicant).where(Applicant.status == "in progress")
        for j in join:
            print(j.applicant.school, j.applicant.first_name, j.time, j.mentor.first_name)
        for m in mentor.mentor_datas:
            print(m.time, m.mentor.first_name)
        for a in app:
            print(a.first_name, a.school.first_name)
        for ai in apps:
            for ad in ai.applicant_datas:
                print(ad.time, ad.mentor.first_name)


Menu.select_option()
