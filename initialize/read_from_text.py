import os.path
import getpass
import json


class Read_from_text:

    exist = os.path.isfile("db_user.json")

    @classmethod
    def create_file(cls):
        if not cls.exist:
            user = input("Please enter your database username: ")
            db_name = input("Please enter your database name:")
            pwd = getpass.getpass(prompt="Enter your password:")

            my_dict = {
                'user': user,
                'db_name': db_name,
                'pwd': pwd
            }

            with open('db_user.json', 'w') as outfile:
                json.dump(my_dict, outfile)

        else:
            my_dict = cls.get_file()

        return my_dict

    @classmethod
    def get_file(cls):
        if cls.exist:
            with open('db_user.json') as json_data:
                user_data = json.load(json_data)

        return user_data
