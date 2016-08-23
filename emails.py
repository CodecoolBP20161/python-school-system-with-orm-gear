class Email():

    @classmethod
    def send_email(cls, recipient, user, pwd, subject, body):
        import smtplib

        gmail_user = user
        gmail_pwd = pwd
        FROM = user
        TO = [recipient]
        SUBJECT = subject
        TEXT = body

        # Prepare actual message
        message = """From: %s\nTo: %s\nSubject: %s\n\n%s
        """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.ehlo()
            server.starttls()
            server.login(gmail_user, gmail_pwd)
            server.sendmail(FROM, TO, message)
            server.close()
            print('successfully sent the mail')
        except:
            print("failed to send mail")

#     @staticmethod
#     def test_email():
#         import smtplib
#
#         user = "girhes.cc.2016@gmail.com"
#         pwd = "Girhes2016"
#         subject = "Testing 1, 2, 3..."
#         body = "This is an automatically generated e-mail to test the mail service."
#
#         gmail_user = user
#         gmail_pwd = pwd
#         FROM = user
#         TO = [user]
#         SUBJECT = subject
#         TEXT = body
#
#         # Prepare actual message
#         message = """From: %s\nTo: %s\nSubject: %s\n\n%s
#         """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
#         try:
#             server = smtplib.SMTP("smtp.gmail.com", 587)
#             server.ehlo()
#             server.starttls()
#             server.login(gmail_user, gmail_pwd)
#             server.sendmail(FROM, TO, message)
#             server.close()
#             print('successfully sent the mail')
#         except:
#             print("failed to send mail")
#
# Email.test_email()
