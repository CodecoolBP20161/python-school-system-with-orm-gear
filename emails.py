
#todo: refactor email, send method with decorator, and get instance method for email send
class Email:

    @staticmethod
    def send_email(recipient, user, pwd, subject, body):
        import smtplib
        # print(recipient, user, pwd, subject, body)
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
            print('E-mail sent successfully TO: {0}'.format(recipient))
        except:
            print("Failed to send e-mail.")
