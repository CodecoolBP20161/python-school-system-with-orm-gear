from flask import *
from functools import *
import os
import datetime
from peewee import *
from read_from_text import *
from main import Main
# from models import *
from model.Applicant import Applicant
from model.BaseModel import db
from model.InterviewSlot import InterviewSlot
from model.Mentor import Mentor
from model.InterviewSlotMentor import InterviewSlotMentor
from model.Email_log import Email_log

from validation import Validation
from controll_admin import admin_page

app = Flask(__name__)
app.register_blueprint(admin_page) # url_prefix='/admin'
# db = PostgresqlDatabase('6_teamwork_week',
#                         **{'user': Read_from_text.connect_data(), 'host': 'localhost', 'port': 5432,
#                            'password': '753951'})
db.connect()
secret = os.urandom(24)
app.secret_key = secret


@app.route('/')
def index():
    return render_template('base.html')



@app.route('/registration', methods=['GET', 'POST'])
def registration_form():
    try:
        applicant = Applicant.create_from_form(request.form)
    except:
        applicant = Applicant(first_name="", last_name="", email="", city="")

    if request.method == "POST":
        validation_result = applicant.valid()
        if len(validation_result) == 0:
            applicant.save()
            Main.get_user_email_data()
            Main.register()
            Main.interview()
            return render_template('base.html', message="Thanks for your registration :)")
        else:
            return render_template('registration.html', applicant=applicant, errors=validation_result)
    return render_template('registration.html', applicant=applicant)


if __name__ == '__main__':
    app.run()
    # app.run(debug=True)
