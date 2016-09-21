from initialize.read_from_text import Read_from_text

class Database_info:
    db_info = Read_from_text.create_file()

    @classmethod
    def db_user_name(cls):
        return cls.db_info['user']

    @classmethod
    def db_name(cls):
        return cls.db_info['db_name']

    @classmethod
    def db_password(cls):
        return cls.db_info['pwd']