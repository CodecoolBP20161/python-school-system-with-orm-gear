class Message:
    @staticmethod
    def message_dict(subject, message):
        return {"subject": subject, "body": message}

    @classmethod
    def new_applicant(cls, first_name, code, school):
        subject = "Codecool application process"
        message = """Dear {0},

                     Your application code is: {1}
                     Your school is: {2}
                     Best Regards,
                     CodeCool   """.format(first_name, code, school)

        return cls.message_dict(subject, message)

    @classmethod
    def applicant_interview(cls, first_name, time, mentor_first_name, mentor_last_name):
        subject = "Codecool"
        message = """Dear {0},

                     Your interview time slot is: {1}
                     Your mentor's name is: {2} {3}
                     Best Regards,
                     Codecool   """.format(first_name, time, mentor_first_name, mentor_last_name)

        return cls.message_dict(subject, message)

    @classmethod
    def mentor_interview(cls, first_name, time, applicant_first_name, applicant_last_name):
        subject = "Codecool interview information"
        message = """Dear {0},

                         Your interview time slot is: {1}
                         Your applicant's name is: {2} {3}
                         Best Regards,
                         Codecool   """.format(first_name, time, applicant_first_name, applicant_last_name)

        return cls.message_dict(subject, message)
