import os.path
import getpass
import json


class UserDataJson:
    user_data = None
    exist = os.path.isfile("db_user.json")

    @classmethod
    def create_file(cls):
        if not cls.exist:
            db_user = input("Please enter your database username: ")
            db_name = input("Please enter your database name:")
            db_pwd = getpass.getpass(prompt="Enter your password:")
            email_user = input("Please enter the central email address: ")
            email_pwd = getpass.getpass(prompt="Enter your password:")

            my_dict = {
                'database': {
                    'user': db_user,
                    'db_name': db_name,
                    'pwd': db_pwd
                },
                'user': {
                    'user': email_user,
                    'pwd': email_pwd
                }
            }

            with open('db_user.json', 'w') as outfile:
                json.dump(my_dict, outfile)
                outfile.close()

        else:
            my_dict = cls.get_file()

        cls.user_data = my_dict
        return my_dict

    @classmethod
    def get_file(cls):
        if cls.exist:
            with open('db_user.json') as json_data:
                user_data = json.load(json_data)
                cls.user_data = user_data
        return user_data

