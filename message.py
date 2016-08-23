class Message:

    @classmethod
    def new_applicant(cls, first_name, code, school):
        subject = "Codecool application process"
        message = """Dear {0},

                     Your application code is: {1}
                     Your school is: {2}
                     Best Regards,
                     CodeCool   """.format(first_name, code, school)

        message_dict = {"subject": subject,
                        "body": message
                        }
                      
        return message_dict

    @classmethod
    def apllicant_interview(cls, first_name, time, mentor_first_name, mentor_last_name):
        subject = "Codecool interview information"
        message = """Dear {0},

                     Your interview time slot is: {1}
                     Your mentor is: {2} {3}
                     Best Regards,
                     Codecool   """.format(first_name, time, mentor_first_name, mentor_last_name)

        message_dict = {"subject": subject,
                        "body": message
                        }

        return message_dict
