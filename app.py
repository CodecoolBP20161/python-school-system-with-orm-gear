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
        else:
            for key, values in validation_result.items():
                flash(values)
    return render_template('registration.html', applicant=applicant)

# @app.route('/registration', methods=['POST', 'GET'])
# def register():
#     applicant = Applicant.create_from_form(request.form)
#     if Validation.first_name_validation(applicant) is True:
#         if Validation.last_name_validation(applicant) is True:
#             if Validation.e_mail_exist(applicant) is True:
#                 applicant = Applicant.create(first_name=request.form['first_name'],
#                                              last_name=request.form['last_name'],
#                                              email=request.form['email'],
#                                              city=request.form['city'])
#                 flash('Thanks for your registration')
#             else:
#                 flash('E-mail already in use')
#         else:
#             flash('Invalid last name')
#     else:
#         flash('Invalid first name')
#         data = Applicant(first_name=request.form['first_name'],
#                          last_name=request.form['last_name'],
#                          email=request.form['email'],
#                          city=request.form['city'])
#         return redirect(get_url('/registration',
#                                 request.form['first_name'],
#                                 request.form['last_name'],
#                                 request.form['email'],
#                                 request.form['city']))
#     return redirect('/registration')


if __name__ == '__main__':
    # app.run()
    app.run(debug=True)
