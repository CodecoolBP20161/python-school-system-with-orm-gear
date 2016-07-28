# This script can create the database tables based on your models

from models import *

db.connect()
# List the tables here what you want to create...
db.drop_tables([Person, Applicant, City, Mentor, InterviewSlot], safe=True)
db.create_tables([Person, Applicant, City, Mentor, InterviewSlot], safe=True)
