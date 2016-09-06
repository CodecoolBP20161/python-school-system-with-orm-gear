from flask import *
from models import *

app = Flask(__name__)
db.connect()

app = Flask(__name__)

HOST = 'http://localhost:5000/'

@app.route('/')
def index():
    return 'Hello flask!'

@app.route('/registration', methods=['GET'])
def registration_form():
    empty_object = Applicant(first_name="", last_name="", email="", city="")
    return render_template('registration.html', applicant = empty_object)

@app.route('/registration', methods=['POST'])
def register():
    data = Applicant.create(first_name=request.form['first_name'],
                            last_name=request.form['last_name'],
                            email=request.form['email'],
                            city=request.form['city'])
    return 'Registration sent.'


if __name__ == '__main__':
    app.run(debug=True)
