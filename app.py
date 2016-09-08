from flask import *
from models import *
import json
from validation import Validation
from functools import *
import os

app = Flask(__name__)
db.connect()

secret = os.urandom(24)
DEBUG = True
app.secret_key = secret
USERNAME = 'admin'
PASSWORD = 'default'


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('username') is None:
            return redirect(url_for('index', next=request.url))
        return f(*args, **kwargs)

    return decorated_function


@app.route('/')
def index():
    applicant_filter = InterviewSlot.select(InterviewSlot, InterviewSlotMentor, Mentor, Applicant).join(
        InterviewSlotMentor).join(
        Mentor).switch(InterviewSlot).join(Applicant).where(~(InterviewSlot.applicant >> None))

    for i in applicant_filter:
        print(i.time, i.detail, i.applicant.first_name)

    return render_template('index.html')


@app.route('/registration', methods=['GET', 'POST'])
def registration_form():
    try:
        applicant = Applicant.create_from_form(request.form)
    except:
        applicant = Applicant(first_name="", last_name="", email="", city="")

    if request.method == "POST":
        validation_result = applicant.valid()
        if (len(validation_result) == 0):
            applicant.save()
            return render_template('index.html', message="Thanks for your registration :)")

        else:
            return render_template('registration.html', applicant=applicant, errors=validation_result)
    return render_template('registration.html', applicant=applicant)


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    with open('admin.json') as json_data:
        admin_data = json.load(json_data)
        print(admin_data['username'], "json")
    if request.method == "POST":
        print(request.form['username'], "post")
        if request.form['username'] != admin_data['username']:
            flash('Wrong user name')
            return render_template('login.html')
        elif request.form['password'] != admin_data['password']:
            flash('Wrong passworld')
            return render_template('login.html')
        else:
            session['username'] = request.form['username']
            flash("You have logged in. Welcome on the board")
            return redirect(url_for('admin_filter'))

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    session.pop('username', None)
    # flash('You were logged out')
    return 'You were logged out'


@app.route('/admin/applicant_list', methods=['GET', 'POST'])
@login_required
def admin_filter():
    forms = request.form.to_dict()

    schools = Applicant.select(Applicant.school).group_by(Applicant.school)
    statuses = Applicant.select(Applicant.status).group_by(Applicant.status)
    cities = Applicant.select(Applicant.city).group_by(Applicant.city)
    mentors = Mentor.select(Mentor.first_name, Mentor.last_name).group_by(Mentor.first_name, Mentor.last_name)

    if request.method == "POST":
        applicant_filter = Applicant.select()
        # print(forms)

        if forms.get('mentor') and len(forms.get('mentor')) > 0:
            full_name = forms.get('mentor').split(" ")
            applicant_filter = Applicant.select(Applicant, InterviewSlot, InterviewSlotMentor, Mentor).join(
                InterviewSlot).join(
                InterviewSlotMentor).join(Mentor).where(Mentor.first_name.contains(full_name[0]),
                                                        Mentor.last_name.contains(full_name[1]))
        if forms.get('time_to') and forms.get('time_from'):
            applicant_filter = applicant_filter.where(
                getattr(Applicant, 'registration_time') > datetime.strptime(forms.get('time_from'), "%Y-%m-%d"),
                getattr(Applicant, 'registration_time') < datetime.strptime(forms.get('time_to'), "%Y-%m-%d"))

        for key, value in forms.items():
            # print(len(value))
            if key != "mentor" and key != "time_from" and key != "time_to" and len(value) > 0:
                applicant_filter = applicant_filter.where(
                    getattr(Applicant, key).contains(value))

        return render_template('applicant.html', applicant_filter=applicant_filter, schools=schools, statuses=statuses,
                               cities=cities, mentors=mentors)
    return render_template('applicant.html', schools=schools, statuses=statuses, cities=cities, mentors=mentors)


@app.route('/admin/interview_list', methods=['GET', 'POST'])
# @login_required
def admin_filter_interviews():
    forms = request.form.to_dict()

    schools = InterviewSlot.select(InterviewSlot.school).group_by(InterviewSlot.school)
    mentors = Mentor.select(Mentor.first_name, Mentor.last_name).group_by(Mentor.first_name, Mentor.last_name)

    if request.method == 'POST':
        # if forms.get('school') and len(forms.get('school')) > 0:
        #     interview_filter = InterviewSlot.select(InterviewSlot, InterviewSlotMentor, Mentor, Applicant).join(
        #         InterviewSlotMentor).join(Mentor).switch(InterviewSlot).join(Applicant)
        #     for i in interview_filter:
        #         print(i.interviewslotmentor.mentor.first_name)

        interview_filter = InterviewSlot.select(InterviewSlot, InterviewSlotMentor, Mentor, Applicant).join(
                InterviewSlotMentor).join(
                Mentor).switch(InterviewSlot).join(Applicant)

        if forms.get('mentor') and len(forms.get('mentor')) > 0:
            full_name = forms.get('mentor').split(" ")
            interview_filter = interview_filter.where(~(InterviewSlot.applicant >> None),
                                                                    Mentor.first_name.contains(full_name[0]),
                                                                    Mentor.last_name.contains(full_name[1]))

        if forms.get('time_to') and forms.get('time_from'):
            interview_filter = interview_filter.where(
                InterviewSlot.time > datetime.strptime(forms.get('time_from'), "%Y-%m-%d"),
                InterviewSlot.time < datetime.strptime(forms.get('time_to'), "%Y-%m-%d"))

        if forms.get('code') and len(forms.get('code')) > 0:
            interview_filter = interview_filter.where(
                Applicant.code.contains((forms.get('code'))))

        if forms.get("school") and len(forms.get("school")) > 0:
            interview_filter = interview_filter.where(InterviewSlot.school == forms.get("school"))

        return render_template('interview.html', interview_filter=interview_filter, schools=schools, mentors=mentors)

    return render_template('interview.html', schools=schools, mentors=mentors)


@app.route('/admin/e-mail-log')
@login_required
def email_log():
    email = Email_log.select()
    return render_template('email_table.html', email=email)


if __name__ == '__main__':
    # app.run()
    app.run(debug=True)
