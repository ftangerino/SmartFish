from flask import Flask, render_template, request, redirect, session
import requests
import json
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['smart-fish']
collection = db['fishes_information']
user_collection = db['user_information']

app = Flask(__name__)
app.secret_key = '18092ASDFdsagf23sdg089ASRF09gs12580GfgWD9035'

def send_token(phone):
    try:
        response = requests.get(f"http://localhost:3000/sendToken?phone={phone}")
        response.raise_for_status()
        print("Token enviado com sucesso")
    except Exception as err:
        print(f"Erro ao enviar token: {err}")

# def limpar_tokens_expirados():
#     current_time = datetime.now()
#     expired_tokens = collection.delete_many({'expiry_time': {'$lt': current_time}})
#     print(f"Tokens expirados removidos: {expired_tokens.deleted_count}")

#limpar_tokens_expirados()

def verify_token(phone, token):
    client = MongoClient('localhost', 27017)
    db = client['smart-fish']
    collection = db['tokens_with_numbers']
    user = collection.find_one({'phone': phone, 'token': token})
    return user is not None

def is_valid_phone(phone):
    return user_collection.find_one({'phone': phone}) is not None

def phone_exists(phone):
    client = MongoClient('localhost', 27017)
    db = client['smart-fish']
    collection = db['user_information']
    user = collection.find_one({'phone': phone})
    return user is not None


def save_user_info(info):
    user_collection.insert_one(info)

def save_bulk_fishes(info):
    collection.insert_one(info)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', phone_exists=None)
    elif request.method == 'POST':
        phone = request.form['phone']
        if request.form.get('send_token'):
            if phone_exists(phone):
                send_token(phone)
                return render_template('login.html', phone_exists=True)
            else:
                return render_template('login.html', phone_exists=False)
        elif request.form.get('login'):
            token = request.form['token']
            if verify_token(phone, token):
                # Autenticado com sucesso
                session['logged_in'] = True
                return redirect('/index')
            else:
                return "Token inválido. Por favor, tente novamente."

@app.route('/')
def redirect_to_select():
    return redirect('/select')

@app.route('/select', methods=['GET'])
def select():
    return render_template('select.html')

# Rota para processar a escolha do usuário
@app.route('/select', methods=['POST'])
def select_action():
    choice = request.form['choice']
    if choice == 'register':
        return redirect('/register')
    elif choice == 'login':
        return redirect('/login')
    else:
        return "Escolha inválida"

@app.route('/register', methods=['GET'])
def register():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
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

@app.route('/registration_success', methods=['GET'])
def registration_success():
    return render_template('registration_success.html')


#########################    

@app.route('/index')
def index():
    if 'logged_in' in session and session['logged_in']:
        return render_template('index.html')
    else:
        return redirect('/login')

@app.route('/get_fish_info', methods=['POST'])
def get_fish_info():
    fish_name = request.form['fish_name']

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": "Bearer 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",
        },
        data=json.dumps({
            "model": "mistralai/mixtral-8x7b-instruct",
            "messages": [
                {
                    "role": "system",
                    "content": "You will provide information about fish that the user enters. You always need to provide a short sentence about the fish, the amount of food it eats, pH of water, and how often it should be fed (provide these pieces of information separately), always provide quantity and period in numbers such as weight (not in percentage of weight but in grams that he should consume, if you don't know how to do the conversion), pH of water, and hours. If the provided fish doesn't consume food, add the type of food it consumes. If you don't know, answer that this fish doesn't exist in the database. If the fish is not suitable for farming in an aquarium, just send a notification back to the user stating this and ignore all the rest of the instructions. Give me all this information separately, like: Nome do Peixe: ; Tipo de Alimentação: ; Quantidade: ; Período que deve ser alimentado: ; pH d'Água: ; Descrição: . Always answer in portuguese (pt-br). "
                },
                {
                    "role": "user",
                    "content": f"preciso de informações acerca do peixe {fish_name}"
                },
            ],
            "top_p": 1,
            "temperature": 0,
            "frequency_penalty": 0,
            "presence_penalty": 0,
            "repetition_penalty": 1,
            "top_k": 1,
        })
    )

    if response.status_code == 200:
        data = response.json()
        choices = data["choices"]
        if choices:
            content = choices[0]["message"]["content"]
            lines = content.split(";")
            info = {}
            for part in content.split(";"):
                key, value = part.split(":")
                info[key.strip()] = value.strip()
            save_bulk_fishes(info)
            return render_template('index.html', content=lines, error=None)
        else:
            return render_template('index.html', content=None, error="Este peixe não existe na base de dados.")
    else:
        return render_template('index.html', content=None, error="Ocorreu um erro na solicitação.")
    pass

if __name__ == '__main__':
    app.run(debug=True)
