from model.BaseModel import *

class Person(BaseModel):
    first_name = CharField()
    last_name = CharField()
    school = CharField(default='', null=True)
    email = CharField()

    @property
    def full_name(self):
        return ' '.join([self.first_name, self.last_name])
