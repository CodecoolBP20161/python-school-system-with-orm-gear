from peewee import *
from read_from_text import *

# db = PostgresqlDatabase('6_teamwork_week', user=Read_from_text.connect_data())
db = PostgresqlDatabase('6_teamwork_week',
                        **{'user': Read_from_text.connect_data(), 'host': 'localhost', 'port': 5432,
                           'password': '753951'})


class BaseModel(Model):
    """A base model that will use our Postgresql database"""

    class Meta:
        database = db