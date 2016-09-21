from flask import *

from controll_user import user_page
from controller.controll_admin import admin_page
from initialize.read_from_text import *
from model.BaseModel import db

app = Flask(__name__)
app.register_blueprint(admin_page)  # url_prefix='/admin'
app.register_blueprint(user_page)

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
