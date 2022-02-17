from peewee import *

database = SqliteDatabase('db/doxdata.db')

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class DoxUserData(BaseModel):
    profile = TextField(null=True)
    resettable = IntegerField(null=True)
    user_id = IntegerField(null=True)

    class Meta:
        table_name = 'DoxUserData'
        primary_key = False

