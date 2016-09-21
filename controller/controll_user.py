from flask import Blueprint, render_template, request
from model.Applicant import Applicant
from main import Main

user_page = Blueprint('user_page', __name__,
                      template_folder='./templates')


@user_page.route('/')
def index():
    return render_template('base.html')


@user_page.route('/registration', methods=['GET', 'POST'])
def registration_form():
    try:
        applicant = Applicant.create_from_form(request.form)
    except:
        applicant = Applicant(first_name="", last_name="", email="", city="")

    if request.method == "POST":
        validation_result = applicant.valid()
        if len(validation_result) == 0:
            applicant.save()
            Main.register()
            return render_template('base.html', message="Thanks for your registration :)")
        else:
            return render_template('registration.html', applicant=applicant, errors=validation_result)
    return render_template('registration.html', applicant=applicant)
