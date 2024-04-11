from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['smart-fish']
collection = db['fishes_information']
user_collection = db['user_information']

def is_valid_phone(phone):
    return user_collection.find_one({'phone': phone}) is not None

def phone_exists(phone):
    client = MongoClient('localhost', 27017)
    db = client['smart-fish']
    collection = db['user_information']
    user = collection.find_one({'phone': phone})
    return user is not None