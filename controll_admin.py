from flask import Blueprint, render_template, request, session, redirect, url_for
from validation import Validation
from model.Applicant import Applicant
from model.InterviewSlot import InterviewSlot
from model.Mentor import Mentor
from model.InterviewSlotMentor import InterviewSlotMentor
from model.Email_log import Email_log
# from jinja2 import TemplateNotFound
from functools import wraps

admin_page = Blueprint('admin_page', __name__,
                       template_folder='templates')


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('username') is None:
            return redirect(url_for('index', next=request.url))
        return f(*args, **kwargs)

    return decorated_function


# @admin_page.route('/', defaults={'page': 'index'})
# @admin_page.route('/<page>')

@admin_page.route('/admin', methods=['GET', 'POST'])
def admin():
    result = render_template('login.html')
    if request.method == "POST":
        errors = {}
        username = request.form['username']
        if not Validation.username_correct(username):
            errors['username'] = 'Wrong username'
        if not Validation.password_correct(request.form['password']):
            errors['password'] = 'Wrong password'
        if len(errors) == 0:
            session['username'] = username
            result = redirect('/')
        else:
            result = render_template('login.html', errors=errors)
    return result


@admin_page.route('/logout')
@login_required
def logout():
    session.pop('username', None)
    return render_template('base.html', message="You were logged out")


@admin_page.route('/admin/applicant_list', methods=['GET', 'POST'])
@login_required
def admin_filter():
    forms = request.form.to_dict()

    applicant_groups = ['school', 'status', 'city']
    applicant_options = Applicant.option_groups(applicant_groups)
    mentors_options = Mentor.select(Mentor.first_name, Mentor.last_name).group_by(Mentor.first_name, Mentor.last_name)

    if request.method == "POST":
        applicant_filter = Applicant.select()
        from_time = forms.get('time_from')
        to_time = forms.get('time_to')

        if forms.get('mentor') and len(forms.get('mentor')) > 0:
            full_name = forms.get('mentor').split(" ")

            applicant_filter = Applicant.select(Applicant, InterviewSlot, InterviewSlotMentor, Mentor).join(
                InterviewSlot).join(
                InterviewSlotMentor).join(Mentor).where(Mentor.first_name.contains(first_name),
                                                        Mentor.last_name.contains(last_name))

        if to_time or from_time:
            if from_time:
                applicant_filter = applicant_filter.where(
                    getattr(Applicant, 'registration_time') > datetime.strptime(from_time, "%Y-%m-%d"))
            elif to_time:
                applicant_filter = applicant_filter.where(
                    getattr(Applicant, 'registration_time') < datetime.strptime(to_time, "%Y-%m-%d"))

        if to_time and from_time:
            applicant_filter = applicant_filter.where(
                getattr(Applicant, 'registration_time') > datetime.strptime(from_time, "%Y-%m-%d"),
                getattr(Applicant, 'registration_time') < datetime.strptime(to_time, "%Y-%m-%d"))

        for key, value in forms.items():
            if key != "mentor" and key != "time_from" and key != "time_to" and len(value) > 0:
                applicant_filter = applicant_filter.where(
                    getattr(Applicant, key).contains(value))

        return render_template('applicant.html', applicant_filter=applicant_filter, schools=applicant_options[0],
                               statuses=applicant_options[1],
                               cities=applicant_options[2], mentors=mentors_options)
    return render_template('applicant.html', schools=applicant_options[0], statuses=applicant_options[1],
                           cities=applicant_options[2],
                           mentors=mentors_options)


@admin_page.route('/admin/interview_list', methods=['GET', 'POST'])
@login_required
def admin_filter_interviews():
    forms = request.form.to_dict()

    schools = InterviewSlot.select(InterviewSlot.school).group_by(InterviewSlot.school)
    # interview_groups = ['school']
    # schools = InterviewSlot.option_groups(interview_groups)
    mentors = Mentor.select(Mentor.first_name, Mentor.last_name).group_by(Mentor.first_name, Mentor.last_name)

    if request.method == 'POST':

        interview_filter = InterviewSlot.select(InterviewSlot, InterviewSlotMentor, Mentor, Applicant).join(
            InterviewSlotMentor).join(
            Mentor).switch(InterviewSlot).join(Applicant)

        if forms.get('mentor') and len(forms.get('mentor')) > 0:
            full_name = forms.get('mentor').split(" ")
            interview_filter = interview_filter.where(~(InterviewSlot.applicant >> None),
                                                      Mentor.first_name.contains(full_name[0]),
                                                      Mentor.last_name.contains(full_name[1]))

        if forms.get('time_to') or forms.get('time_from'):
            if forms.get('time_from'):
                interview_filter = interview_filter.where(
                    InterviewSlot.time > datetime.strptime(forms.get('time_from'), "%Y-%m-%d"))
            elif forms.get('time_to'):
                interview_filter = interview_filter.where(
                    InterviewSlot.time < datetime.strptime(forms.get('time_to'), "%Y-%m-%d"))

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


@admin_page.route('/admin/e-mail-log')
@login_required
def email_log():
    email = Email_log.select()
    return render_template('email_table.html', email=email)
