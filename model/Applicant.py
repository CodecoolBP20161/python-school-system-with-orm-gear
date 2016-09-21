import random
from datetime import *
from peewee import CharField, TextField, DateTimeField
from model.City import City
from model.Person import Person
from model.Email_log import EmailLog
from model.Send_email.emails import Email
from model.Send_email.message import Message


class Applicant(Person):
    code = CharField(default=None, null=True, unique=True)
    city = TextField()
    status = CharField(default='new')
    registration_time = DateTimeField(default=datetime.utcnow())

    @classmethod
    def update_school(cls):
        new_applicant = cls.filter("status", "new")
        if new_applicant:
            for applicant in new_applicant:
                school_get = City.get(City.applicant_city == applicant.city)
                applicant.school = school_get.school
                applicant.save()

    @classmethod
    def get_codes(cls):
        codes = []
        get_codes = cls.select(cls.code).where(~(cls.code >> None)).tuples()
        for code in get_codes:
            codes.append(codes)
        return codes

    def new_code(self):
        while True:
            new_code = "".join([self.school[:2].upper(), str(random.randint(1000, 10000))])
            if new_code not in Applicant.get_codes():
                break
        return new_code

    @classmethod
    def set_code(cls):
        get_applicant = cls.filter("code", None)
        for applicant in get_applicant:
            applicant.code = applicant.new_code()
            applicant.save()
            print(applicant.code, applicant.first_name, applicant.last_name, applicant.city, applicant.school,
                  applicant.status, applicant.email)

    @classmethod
    def get_assigned_applicants(cls):
        return cls.select().where(~(cls.code >> None), ~(cls.school >> None), cls.status == "new")

    @classmethod
    def create_from_form(cls, request_form):
        return Applicant(first_name=request_form['first_name'],
                         last_name=request_form['last_name'],
                         email=request_form['email'],
                         city=request_form['city'])

    def valid(self):
        from controller.validation import Validation
        errors = {}
        if Validation.first_name_validation(self.first_name):
            errors['first_name'] = 'Invalid'
        if Validation.last_name_validation(self.last_name):
            errors['last_name'] = 'Invalid'
        if Validation.email_exists(self.email):
            errors['email'] = 'already in use'
        return errors

    @classmethod
    def send_mail_for_new_applicant(cls):
        for applicant in cls.get_assigned_applicants():
            message_dict = Message(applicant.first_name, applicant.code, applicant.school)
            message_dict = message_dict.new_applicant()
            sent_email = Email(applicant.email, **message_dict)
            sent_email.send_mail()
            # print(message_dict['subject'])
#todo: to the email log to send from it the email, facade or decorator new class???
            EmailLog.create_email_log(message_dict['subject'], message_dict['body'], "new applicant",
                                       datetime.utcnow(), applicant.full_name, applicant.email)

    def get_applicant_details_for_interview(self):
        from model.InterviewSlot import InterviewSlot
        from model.InterviewSlotMentor import InterviewSlotMentor
        from model.Mentor import Mentor
        details = {"mentors": []}
        for mentor in Applicant.select(Applicant, InterviewSlot, InterviewSlotMentor, Mentor).join(
                InterviewSlot).join(InterviewSlotMentor).join(Mentor).where(self.id == Applicant.id):
            details["mentors"].append(mentor.full_name)
            details["time"] = mentor.interviewslot.time
        return details
#todo: some problem precess is sending emails again and again don't know who has received email
    @classmethod
    def send_applicant_interview_email(cls):
        for applicant in cls.filter("status", "processing"):
            details = applicant.get_applicant_details_for_interview()
            message_dict = Message(applicant.first_name, details["time"],
                                   details["mentors"][0],details["mentors"][1])
            message_dict = message_dict.applicant_interview()
            sent_email = Email(applicant.email, **message_dict)
            sent_email.send_mail()
            EmailLog.create_email_log(message_dict['subject'], message_dict['body'], "applicant's interview",
                                       datetime.utcnow(), applicant.full_name, applicant.email)



