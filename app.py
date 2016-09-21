from flask import *

from controller.controll_admin import admin_page
from controller.controll_user import user_page
from initialize.read_from_text import *
from model.BaseModel import db

app = Flask(__name__)
app.register_blueprint(admin_page)  # url_prefix='/admin'
app.register_blueprint(user_page)

secret = os.urandom(24)
app.secret_key = secret

