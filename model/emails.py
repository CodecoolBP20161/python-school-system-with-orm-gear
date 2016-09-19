import smtplib
from initialize.user import User

#todo: refactor email, send method with decorator, and get instance method for email send


class Email:
    user_data = User.create_file()

    def __init__(self, recipient, subject, body):
        self.recipient = recipient
        self.subject = subject
        self.body = body
        self.user = Email.user_data['user']
        self.pwd = Email.user_data['pwd']


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
