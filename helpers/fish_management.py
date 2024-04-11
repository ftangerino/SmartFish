import requests
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['smart-fish']
collection = client['fishes_information']

def save_bulk_fishes(info):
    collection.insert_one(info)

