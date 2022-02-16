import json
import peewee
from db.dbmodels import *
import utils
import json


def set_profile(user_id: int, profile:str):
    query = DoxUserData.select().where(DoxUserData.user_id == user_id)
    if len(query) == 0:
        DoxUserData.create(user_id=user_id, profile=profile)
    elif len(query) == 1:
        new_query = DoxUserData.update(profile=profile).where(DoxUserData.user_id == user_id)
        new_query.update()

def get_profile(user_id: int):
    query = DoxUserData.select().where(DoxUserData.user_id == user_id)
    if len(query) == 0:
        set_profile(user_id, utils.get_fake_profile())
        return get_profile(user_id)
    elif len(query) == 1:
        for item in query:
            profile = item.profile
            json_compatible= profile.replace("'", "\"")
            profile_dict = json.loads(json_compatible)
            return profile_dict