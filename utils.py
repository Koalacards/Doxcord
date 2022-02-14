from faker import Faker
from faker.providers import internet
from faker.providers import phone_number
import discord
def get_fake_ip() -> str:
    fake = Faker()
    fake.add_provider(internet)
    return fake.ipv4_private()

def get_fake_address():
    fake = Faker()
    return fake.address()

def get_fake_phone_number():
    fake = Faker()
    fake.add_provider(phone_number)
    return fake.phone_number()

def get_fake_name():
    fake = Faker()
    return fake.name()

def create_embed(title:str, description:str, color: discord.Color):
    embed = discord.Embed(
        title=title,
        description=description,
        color=color
    )
    return embed