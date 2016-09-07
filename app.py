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
            render_template('index.html')
            flash("Thanks for your registration :)")
            return
        else:
            for key, values in validation_result.items():
                flash(values)
    return render_template('registration.html', applicant=applicant)



@app.route('/admin/e-mail-log')
def email_log():
    email = Email_log.select()
    return render_template('email_table.html', email=email)

if __name__ == '__main__':
    # app.run()
    app.run(debug=True)
