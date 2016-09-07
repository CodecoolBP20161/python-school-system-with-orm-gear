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
    return render_template('index.html')


@app.route('/registration', methods=['GET', 'POST'])

def registration_form():
    try:
        applicant = Applicant.create_from_form(request.form)
    except:
        applicant = Applicant(first_name="", last_name="", email="", city="")

    if request.method == "POST":
        validation_result = applicant.valid()
        if(len(validation_result) == 0):
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


    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    # flash('You were logged out')
    return 'You were logged out'


@app.route('/admin/e-mail-log')
@login_required
def email_log():
    email = Email_log.select()
    return render_template('email_table.html', email=email)


if __name__ == '__main__':
    app.run()
    # app.run(debug=True)
