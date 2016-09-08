from flask import *
from models import *
import json
from functools import *
import os

app = Flask(__name__)
db.connect()
secret = os.urandom(24)
app.secret_key = secret


@app.route('/')
def index():
    return render_template('base.html')


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('username') is None:
            return redirect(url_for('index', next=request.url))
        return f(*args, **kwargs)

    return decorated_function


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
            return render_template('base.html', message="Thanks for your registration :)")
        else:
            return render_template('registration.html', applicant=applicant, errors=validation_result)
    return render_template('registration.html', applicant=applicant)


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    result = render_template('login.html')
    with open('admin.json') as json_data:
        admin_data = json.load(json_data)

    if request.method == "POST":
        username = request.form['username']

        if username != admin_data['username']:
            flash('Wrong user name')
        elif request.form['password'] != admin_data['password']:
            flash('Wrong password')
        else:
            session['username'] = username
            result = redirect(url_for('admin_filter'))

    return result


@app.route('/logout')
@login_required
def logout():
    session.pop('username', None)
    return render_template('base.html', message="You were logged out")



@app.route('/admin/applicant_list', methods=['GET', 'POST'])
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
            applicant_filter = Applicant.mentors_for_applicant(full_name[0], full_name[1])

        if to_time and from_time:
            applicant_filter = applicant_filter.registered_applicant_between_given_time(from_time, to_time)

        for key, value in forms.items():
            if key != "mentor" and key != "time_from" and key != "time_to" and len(value) > 0:
                applicant_filter = applicant_filter.where(
                    getattr(Applicant, key).contains(value))

        return render_template('applicant.html', applicant_filter=applicant_filter, schools=applicant_options[0],
                               statuses=applicant_options[1],
                               cities=applicant_options[2], mentors=mentors_options)
    return render_template('applicant.html', schools=applicant_options[0], statuses=applicant_options[1], cities=applicant_options[2],
                           mentors=mentors_options)


@app.route('/admin/e-mail-log')
@login_required
def email_log():
    email = Email_log.select()
    return render_template('email_table.html', email=email)


if __name__ == '__main__':
    # app.run()
    app.run(debug=True)
