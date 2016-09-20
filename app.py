from flask import *

from controller.controll_admin import admin_page

from initialize.read_from_text import *
from main import Main

from model.Applicant import Applicant
from model.BaseModel import db


app = Flask(__name__)
app.register_blueprint(admin_page) # url_prefix='/admin'

secret = os.urandom(24)
app.secret_key = secret



@app.before_first_request
def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'postgres_db'):
        g.postgres_db = db.connect()


    return g.postgres_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'postgres_db'):
        g.postgres_db.close()


@app.route('/')
def index():
    return render_template('base.html')



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
            Main.register()
            return render_template('base.html', message="Thanks for your registration :)")
        else:
            return render_template('registration.html', applicant=applicant, errors=validation_result)
    return render_template('registration.html', applicant=applicant)
