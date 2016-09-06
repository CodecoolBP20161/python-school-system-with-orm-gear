from flask import *
from models import *
from validation import Validation
import os
app = Flask(__name__)
db.connect()



secret = os.urandom(24)
DEBUG = True
app.secret_key = secret
USERNAME = 'admin'
PASSWORD = 'default'

@app.route('/')
def index():
    return 'Hello flask!'

@app.route('/registration', methods=['GET'])
def registration_form():
    empty_object = Applicant(first_name="", last_name="", email="", city="")
    return render_template('registration.html', applicant=empty_object)

@app.route('/registration', methods=['POST'])
def register():
    test = Validation(request.form['first_name'], request.form['last_name'], request.form['email'])
    if Validation.first_name_validation(test) is True:
        if Validation.last_name_validation(test) is True:
            if Validation.e_mail_exist(test) is True:
                data = Applicant.create(first_name=request.form['first_name'],
                                        last_name=request.form['last_name'],
                                        email=request.form['email'],
                                        city=request.form['city'])
                flash('Thanks for your registration')
            else:
                flash('E-mail already in use')
        else:
            flash('Invalid last name')
    else:
        flash('Invalid first name')
    return redirect('/registration')

@app.route('/admin/e-mail-log')
def email_log():
    email = Email_log.select()
    return render_template('email_table.html', email=email)

if __name__ == '__main__':
    app.run()
    # app.run(debug=True)
