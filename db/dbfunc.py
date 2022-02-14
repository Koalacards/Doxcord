from audioop import add
import peewee
from db.dbmodels import *
import utils


def set_attributes(user_id: int, ip_address: str, address:str, phone_number: str, name:str):
    query = DoxUserData.select().where(DoxUserData.user_id == user_id)
    if len(query) == 0:
        DoxUserData.create(user_id=user_id, ip_address=ip_address, address=address, phone_number=phone_number, name=name)
    elif len(query) == 1:
        new_query = DoxUserData.update(ip_address=ip_address, address=address, phone_number=phone_number, name=name).where(DoxUserData.user_id == user_id)
        new_query.update()

def set_random_attributes(user_id: int):
    ip = utils.get_fake_ip()
    address = utils.get_fake_address()
    phone = utils.get_fake_phone_number()
    name = utils.get_fake_name()
    set_attributes(user_id, ip, address, phone, name)

def get_attributes(user_id: int):
    query = DoxUserData.select().where(DoxUserData.user_id == user_id)
    if len(query) == 0:
        set_random_attributes(user_id)
        return get_attributes(user_id)
    elif len(query) == 1:
        for item in query:
            return {
                "ip": item.ip_address,
                "address": item.address,
                "phone": item.phone_number,
                "name": item.name,
                }
