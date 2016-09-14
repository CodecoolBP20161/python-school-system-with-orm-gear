
# from model.example_data import *
from example_data import *
from build import *
from main import *

from peewee import *


# story11
class Menu:
    @staticmethod
    def select_option():
        available_choices = ['(1) Generate New Database', '(2) Display Applicants', '(3) Application Details',
                             '(4) Interview Details', '(5) Update', '(0) Exit']
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
                Main.get_user_email_data()
                Main.register()
                Main.interview()
            if menu_choice == '2':
                print('_______________________________________\n')
                applicants = Applicant.select()
                for applicant in applicants:
                    print(applicant.code, applicant.first_name, applicant.last_name, applicant.city, applicant.school,
                          applicant.status, applicant.email)
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
                    mentors = existed_applicant.get_mentors_for_interview("mentors")

                    print('Date: {0}\nSchool: {1}\nMentors: {2} {3}, {4} {5}'.format(interview.time,
                                                                                     existed_applicant.school,
                                                                                     mentors[0], mentors[1],
                                                                                     mentors[2], mentors[3]))
                except Applicant.DoesNotExist:
                    print("Unavaible Application Code")
            if menu_choice == '5':
                print('_______________________________________\n')
                Main.register()
                Main.interview()


Menu.select_option()
