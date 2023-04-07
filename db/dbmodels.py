from peewee import *

database = SqliteDatabase('db/doxdata.db')

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class DoxUserData(BaseModel):
    profile = TextField(null=True)
    profile_name = TextField(null=True)
    user_id = IntegerField(null=True)

    class Meta:
        table_name = 'DoxUserData'
        primary_key = False

class UserSelectedProfile(BaseModel):
    selected_profile = TextField(null=True)
    user_id = IntegerField(null=True)

    class Meta:
        table_name = 'UserSelectedProfile'
        primary_key = False

