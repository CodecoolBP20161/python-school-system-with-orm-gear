import json
import os.path
import getpass


class User:

    exist = os.path.isfile("user.json")

    @classmethod
    def create_file(cls):
        if not cls.exist:
            user = input("Please enter the central email address: ")
            pwd = getpass.getpass(prompt="Enter your password:")

            my_dict = {
              'user': user,
              'pwd': pwd
            }

            with open('user.json', 'w') as outfile:
                json.dump(my_dict, outfile)

        else:
            my_dict = cls.get_file()

        return my_dict

    @classmethod
    def get_file(cls):
        if cls.exist:

            with open('user.json') as json_data:
                user_data = json.load(json_data)

        return user_data
