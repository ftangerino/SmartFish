import requests
from pymongo import MongoClient
from flask import Flask, render_template, request, redirect, session

client = MongoClient('localhost', 27017)
user_collection = db['user_information']

def save_user_info(info):
    user_collection.insert_one(info)

def register_user():
    email = request.form['email']
    name = request.form['name']
    phone = request.form['phone']

    # Verificar se já existe um usuário com essas informações
    existing_user = user_collection.find_one({"$or": [{"email": email}, {"name": name}, {"phone": phone}]})

    if existing_user:
        return "Usuário já cadastrado com essas informações."
    else:
        user_info = {"email": email, "name": name, "phone": phone}
        save_user_info(user_info)
        return render_template('registration_success.html', name=name, email=email, phone=phone)