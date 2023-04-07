from typing import List, Optional

from db.dbmodels import *
from fake_profile import get_fake_profile
from utils import str2dict


def set_profile(user_id: int, profile: str, profile_name: str) -> None:
    query = DoxUserData.select().where(
        DoxUserData.user_id == user_id and DoxUserData.profile_name == profile_name
    )
    if len(query) == 0:
        DoxUserData.create(user_id=user_id, profile=profile, profile_name=profile_name)
        set_selected_profile(user_id, profile_name)
    elif len(query) == 1:
        new_query = DoxUserData.update(profile=profile).where(
            DoxUserData.user_id == user_id and DoxUserData.profile_name == profile_name
        )
        new_query.execute()


def get_profile(user_id: int, profile_name: str, create_new=True) -> Optional[dict]:
    query = DoxUserData.select().where(
        DoxUserData.user_id == user_id and DoxUserData.profile_name == profile_name
    )
    if len(query) == 0:
        if create_new:
            set_profile(user_id, str(get_fake_profile()), profile_name)
            return get_profile(user_id, profile_name)
        else:
            return None
    elif len(query) == 1:
        for item in query:
            profile = item.profile
            return str2dict(profile)


def delete_profile(user_id: int, profile_name: str) -> None:
    query = DoxUserData.delete().where(
        DoxUserData.user_id == user_id and DoxUserData.profile_name == profile_name
    )
    query.execute()


def profiles_for_user(user_id: int) -> List[str]:
    profiles = []
    query = DoxUserData.select().where(DoxUserData.user_id == user_id)
    for item in query:
        profiles.append(item.profile_name)
    return profiles


def get_selected_profile(user_id: int) -> str:
    query = UserSelectedProfile.select().where(UserSelectedProfile.user_id == user_id)
    if len(query) == 0:
        # This should only happen if the user has never been doxxed before
        return None
    elif len(query) == 1:
        for item in query:
            return item.selected_profile


def set_selected_profile(user_id: int, selected_profile: str) -> None:
    query = UserSelectedProfile.select().where(UserSelectedProfile.user_id == user_id)
    if len(query) == 0:
        UserSelectedProfile.create(user_id=user_id, selected_profile=selected_profile)
    elif len(query) == 1:
        new_query = UserSelectedProfile.update(selected_profile=selected_profile).where(
            UserSelectedProfile.user_id == user_id
        )
        new_query.execute()
