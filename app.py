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
            return render_template('index.html', message="Thanks for your registration :)")

        else:
            return render_template('registration.html', applicant=applicant, errors=validation_result)
    return render_template('registration.html', applicant=applicant)


if __name__ == '__main__':
    app.run()
    # app.run(debug=True)
