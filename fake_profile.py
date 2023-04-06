from faker import Faker
from faker.providers import internet
from faker.providers import phone_number
from faker.providers import profile

from typing import List
from datetime import date
from discord.app_commands import Choice

def get_fake_profile():
    fake = Faker()
    fake.add_provider(profile)
    profile_dict = fake.profile()
    fake.add_provider(internet)
    fake.add_provider(phone_number)

    profile_dict['ip'] = fake.ipv4_private()
    profile_dict['phone_number'] = fake.phone_number()

    profile_dict = _fake_profile_modifications(profile_dict)
    return profile_dict

def _fake_profile_modifications(profile_dict: dict) -> dict:
    location = profile_dict.get('current_location')
    profile_dict['current_location'] = [float(location[0]), float(location[1])]
    websites = profile_dict.get('website')
    if type(websites) == list:
        profile_dict['website'] = ", ".join(websites)
    birthdate = profile_dict.get('birthdate')
    if type(birthdate) == date:
        profile_dict['birthdate'] = f"{birthdate.month}/{birthdate.day}/{birthdate.year}"
    return profile_dict


def profile_options() -> List[str]:
    return [
        "All Options",
        "name",
        "birthdate",
        "sex",
        "job",
        "address",
        "phone_number",
        "ssn",
        "mail",
        "website",
        "username",
        "ip",
        "current_location",
        "company",
        "residence",
        "blood_group",
    ]

def profile_choices() -> List[Choice]:
    choices = []
    for index, option in enumerate(profile_options()):
        choices.append(Choice(name=option, value=index))

    return choices

def update_profile(profile_dict: dict, option: str) -> dict:
    """Updates an option on the profile (or all of them if "All Options" is given)

    Args:
        profile_dict (dict): existing profile dict
        option (str): Option to choose from, defined in profile_options above

    Returns:
        dict: updated profile dict
    """
    fake = Faker()
    if option == "All Options":
        return get_fake_profile()
    elif option == "ip":
        fake.add_provider(internet)
        profile_dict['ip'] = fake.ipv4_private()
    elif option == "phone_number":
        fake.add_provider(phone_number)
        profile_dict['phone_number'] = fake.phone_number()
    else:
        fake.add_provider(profile)
        second_profile = fake.profile()
        new_value = second_profile[option]
        profile_dict[option] = new_value
        profile_dict = _fake_profile_modifications(profile_dict)
    return profile_dict
