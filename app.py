from flask import *
from models import *
from validation import Validation
import os
app = Flask(__name__)
db.connect()



# HOST = 'http://localhost:5000/'

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
    # first_name = request.form['first_name']
    # last_name = request.form['last_name']
    # email = request.form['email']

    data = Applicant.create(first_name=request.form['first_name'],
                            last_name=request.form['last_name'],
                            email=request.form['email'],
                            city=request.form['city'])
    flash('Thanks for your registration')
    return redirect('/registration')


if __name__ == '__main__':
    app.run(debug=True)
