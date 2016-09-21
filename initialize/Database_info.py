from initialize.read_from_text import UserDataJson

class DatabaseInfo:
    db_info = UserDataJson.create_file()

    @classmethod
    def db_user_name(cls):
        return cls.db_info['database']['user']

    @classmethod
    def db_name(cls):
        return cls.db_info['database']['db_name']

    @classmethod
    def db_password(cls):
        return cls.db_info['database']['pwd']