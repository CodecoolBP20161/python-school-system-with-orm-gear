import smtplib
from initialize.read_from_text import UserDataJson


class Email:
    # user_data = UserDataJson.create_file()

    def __init__(self, recipient, subject, body):
        self.recipient = recipient
        self.subject = subject
        self.body = body
        self.user = UserDataJson.user_data['user']['user']
        self.pwd = UserDataJson.user_data['user']['pwd']


    def send_mail(self):
        # Prepare actual message
        message = """From: %s\nTo: %s\nSubject: %s\n\n%s
        """ % (self.user, ", ".join([self.recipient]), self.subject, self.body)
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.ehlo()
            server.starttls()
            server.login(self.user, self.pwd)
            server.sendmail(self.user, [self.recipient], message)
            server.close()
            print('E-mail sent successfully TO: {0}'.format(self.recipient))
        except:
            print("Failed to send e-mail.")
