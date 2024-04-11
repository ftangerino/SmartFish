import requests
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
user_collection = db['user_information']

def save_user_info(info):
    user_collection.insert_one(info)