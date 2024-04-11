import requests
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client['smart-fish']
collection = db['fishes_information']
user_collection = db['user_information']

def send_token(phone):
    try:
        response = requests.get(f"http://localhost:3000/sendToken?phone={phone}")
        response.raise_for_status()
        print("Token enviado com sucesso")
    except Exception as err:
        print(f"Erro ao enviar token: {err}")

def verify_token(phone, token):
    client = MongoClient('localhost', 27017)
    db = client['smart-fish']
    collection = db['tokens_with_numbers']
    user = collection.find_one({'phone': phone, 'token': token})
    return user is not None

#limpar_tokens_expirados()
# def limpar_tokens_expirados():
#     current_time = datetime.now()
#     expired_tokens = collection.delete_many({'expiry_time': {'$lt': current_time}})
#     print(f"Tokens expirados removidos: {expired_tokens.deleted_count}")