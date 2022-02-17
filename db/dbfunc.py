import json
import peewee
from db.dbmodels import *
import utils
import json


# If they don't have a profile, they won't have a resettable yet
def set_profile(user_id: int, profile: str):
    query = DoxUserData.select().where(DoxUserData.user_id == user_id)
    if len(query) == 0:
        DoxUserData.create(user_id=user_id, profile=profile, resettable=1)
    elif len(query) == 1:
        new_query = DoxUserData.update(profile=profile).where(DoxUserData.user_id == user_id)
        new_query.execute()


# If they don't already have a profile, it will make one for them
def set_resettable(user_id: int, resettable: int):
    query = DoxUserData.select(DoxUserData.profile).where(DoxUserData.user_id == user_id)
    if len(query) == 0:
        DoxUserData.create(user_id=user_id, profile=profile, resettable=resettable)
    elif len(query) == 1:
        new_query = DoxUserData.update(resettable=resettable).where(DoxUserData.user_id == user_id)
        new_query.execute()


def get_profile(user_id: int):
    query = DoxUserData.select(DoxUserData.profile).where(DoxUserData.user_id == user_id)
    if len(query) == 0:
        set_profile(user_id, utils.get_fake_profile())
        return get_profile(user_id)
    elif len(query) == 1:
        for item in query:
            profile = item.profile
            json_compatible = profile.replace("'", "\"")
            profile_dict = json.loads(json_compatible)
            return profile_dict


def get_resettable(user_id: int):
    query = DoxUserData.select(DoxUserData.resettable).where(DoxUserData.user_id == user_id)
    if len(query) == 0:
        set_resettable(user_id, 0)
        return 0
    elif len(query) == 1:
        for item in query:
            return item.resettable
