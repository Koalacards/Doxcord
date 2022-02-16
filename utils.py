from faker import Faker
from faker.providers import internet
from faker.providers import phone_number
from faker.providers import profile
import discord

def get_fake_profile():
    fake = Faker()
    fake.add_provider(profile)
    profile_dict = fake.profile()
    fake.add_provider(internet)
    fake.add_provider(phone_number)
    fake.ipv4_private()
    del profile_dict['birthdate']
    del profile_dict['website']
    del profile_dict['username']
    del profile_dict['mail']
    location = profile_dict.get('current_location')
    profile_dict['current_location'] = [float(location[0]), float(location[1])]
    profile_dict['ip'] = fake.ipv4_private()
    profile_dict['phone_number'] = fake.phone_number()
    return profile_dict

def create_embed(title:str, description:str, color: discord.Color):
    embed = discord.Embed(
        title=title,
        description=description,
        color=color
    )
    return embed