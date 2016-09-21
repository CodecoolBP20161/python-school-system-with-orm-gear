from peewee import *

from initialize.Database_info import DatabaseInfo

# db = PostgresqlDatabase(DatabaseInfo.db_name(), user=DatabaseInfo.db_user_name())
db = PostgresqlDatabase(DatabaseInfo.db_name(),
                        **{'user': DatabaseInfo.db_user_name(), 'host': 'localhost', 'port': 5432,
                           'password': '753951'})


class BaseModel(Model):
    """A base model that will use our Postgresql database"""

    class Meta:
        database = db

    @classmethod
    def filter(cls, attribute, filter):
        try:
            result = cls.select().where(getattr(cls, attribute) == filter)
        except AttributeError:
            result = None
            print(
                "wrong attribute your {0} select().where({0}.{1} == {2}), query is bad".format(cls, attribute, filter))
        return result

    @classmethod
    def option_groups(cls, groups):
        result = []
        for group in groups:
            attribute = getattr(cls, group)
            result.append(cls.select(attribute).group_by(attribute))
        return result