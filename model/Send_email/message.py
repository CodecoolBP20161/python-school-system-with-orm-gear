class Message:
    @classmethod
    def strip_accents(cls, word):
        import unicodedata
        if type(word) == str:
            return ''.join(c for c in unicodedata.normalize('NFD', word) if unicodedata.category(c) != 'Mn')
        else:
            return word

    def __init__(self, receiver, detail1=None, detail2=None, detail3=None):
        self.receiver = Message.strip_accents(receiver)
        self.detail1 = Message.strip_accents(detail1)
        self.detail2 = Message.strip_accents(detail2)
        self.detail3 = Message.strip_accents(detail3)

    def new_applicant(self):
        subject = "Codecool application process"
        message = """Dear {0},

                     Your application code is: {1}
                     Your school is: {2}
                     Best Regards,
                     CodeCool   """.format(self.receiver, self.detail1, self.detail2)

        return {"subject": subject, "body": message, "type": "new_applicant"}

    def applicant_interview(self):
        subject = "Codecool"
        message = """Dear {0},

                     Your interview time slot is: {1}
                     Your mentors' name are: {2}, {3},
                     Best Regards,
                     Codecool   """.format(self.receiver, self.detail1, self.detail2, self.detail3)

        return {"subject": subject, "body": message, "type": "applicant's interview"}

    def mentor_interview(self):
        subject = "Codecool interview information"
        message = """Dear {0},

                         Your interview time slot is: {1}
                         Your applicant's name is: {2} {3}
                         Best Regards,
                         Codecool   """.format(self.receiver, self.detail1, self.detail2, self.detail3)

        return {"subject": subject, "body": message, "type": "mentors's interview"}
