import requests
from pymongo import MongoClient
from flask import Flask, render_template, request, redirect, session, send_from_directory

client = MongoClient('localhost', 27017)
db = client['smart-fish']
collection = db['fishes_information']
user_collection = db['user_information']

app = Flask(__name__)
app.secret_key = '18092ASDFdsagf23sdg089ASRF09gs12580GfgWD9035'

def save_user_info(info):
    user_collection.insert_one(info)

