from build import *
from example_data import *
from main import *
from models import *
from peewee import *


class Menu():

    @staticmethod
    def select_option():
        available_choices = ['(1) Generate Database', '(2) Application Details', '(3) Interview Details', '(0) Exit']
        menu_choice = None
        while menu_choice != '0':
            print('_______________________________________')
            for i in available_choices:
                print(i)
            print('_______________________________________')
            menu_choice = input('Please select a number: ')
            if menu_choice == '1':
                Build()
                Example_data.insert()
                Main.register()
                Main.interview()
            if menu_choice == '2':
                application_code = input('Please enter your Application Code: ')
                try:
                    existed_applicant = Applicant.get(Applicant.code == application_code)
                except Applicant.DoesNotExist:
                    print("Unavaible Application Code")
                print('School: {0}\nStatus: {1}'.format(existed_applicant.school, existed_applicant.status))
            if menu_choice == '3':
                application_code = input('Please enter your Application Code: ')
                try:
                    existed_applicant = Applicant.get(Applicant.code == application_code)
                    interview = InterviewSlot.get(InterviewSlot.applicant == existed_applicant)
                except Applicant.DoesNotExist:
                    print("Unavaible Application Code")
                print('Date: {0}\nSchool: {1}\nMentor: {2} {3}'.format(interview.time, existed_applicant.school, interview.mentor.first_name, interview.mentor.last_name))

Menu.select_option()
