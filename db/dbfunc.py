from db.dbmodels import *
from fake_profile import get_fake_profile
from utils import str2dict

def set_profile(user_id: int, profile: str):
    query = DoxUserData.select().where(DoxUserData.user_id == user_id)
    if len(query) == 0:
        DoxUserData.create(user_id=user_id, profile=profile)
    elif len(query) == 1:
        new_query = DoxUserData.update(profile=profile).where(DoxUserData.user_id == user_id)
        new_query.execute()


def get_profile(user_id: int) -> dict:
    query = DoxUserData.select(DoxUserData.profile).where(DoxUserData.user_id == user_id)
    if len(query) == 0:
        set_profile(user_id, str(get_fake_profile()))
        return get_profile(user_id)
    elif len(query) == 1:
        for item in query:
            profile = item.profile
            return str2dict(profile)
