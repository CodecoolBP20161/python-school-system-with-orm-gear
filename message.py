class Message:

    @classmethod
    def new_applicant(cls, first_name, code, school):
        subject = "Codecool application process"
        message = """Dear {0},
                     Your application code is: {1}
                     Your school is: {2} """.format(first_name, code, school)

        message_dict = {"subject": subject,
                        "body": message
                        }
                      
        return message_dict
