import os
from flask import Flask, render_template, request, redirect, session, send_from_directory
import requests
import json
import serial
from pymongo import MongoClient
from helpers.tokens_management import send_token, verify_token
from helpers.verifications import is_valid_phone, phone_exists
from helpers.register_screen import save_user_info
client = MongoClient('localhost', 27017)
db = client['smart-fish']
collection = db['fishes_information']
user_collection = db['user_information']

app = Flask(__name__)
app.secret_key = '18092ASDFdsagf23sdg089ASRF09gs12580GfgWD9035'


arduino = None

def connect_to_arduino():
    global arduino
    if arduino is None or arduino.is_open == False:
        try:
            arduino = serial.Serial('COM6', 9600, timeout=1)
            print("Conectado ao Arduino!")
        except SerialException as e:
            print(f"Erro ao abrir a porta serial: {e}")
            arduino = None

#safe
# arduino = serial.Serial('COM5', 9600, timeout=1)

# @app.route('/read_from_arduino')
# def read_from_arduino():
#     try:
#         arduino = serial.Serial('COM5', 9600, timeout=1)  # Certifique-se de ajustar a porta e a velocidade corretamente
#     except serial.SerialException as e:
#         return f"Erro ao abrir a porta serial: {e}"

#     try:
#         arduino.open()
#         while True:
#             sleep(0.01)
#             nextchar = arduino.read()
#             if nextchar:
#                 yield nextchar
#     except Exception as e:
#         return f"Erro na leitura da porta serial: {e}"
#     finally:
#         arduino.close()


# @app.route('/static/<path:filename>')
# def serve_static(filename):
#     root_dir = os.path.dirname(os.getcwd())
#     return send_from_directory(os.path.join(root_dir, 'static'), filename)

# def serve_static(filename):
#     root_dir = os.path.dirname(os.getcwd())
#     return send_from_directory(os.path.join(root_dir, 'static'), filename)

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
    
@app.route('/move_servo', methods=['POST'])
def move_servo():
    if request.method == 'POST':
        # Envia o comando para o Arduino via Serial
        arduino.write(b'MOVE\n')
        return "Servo moved"


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

def save_bulk_fishes(info):
    collection.insert_one(info)
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

        # Verifique se a chave "choices" está no data
        if "choices" in data:
            choices = data["choices"]
            if choices:
                content = choices[0]["message"]["content"]
                lines = content.split(";")
                info = {}
                for part in lines:
                    key_value = part.split(":")
                    if len(key_value) == 2:  # Certifique-se de que há um par chave-valor válido
                        key, value = key_value
                        info[key.strip()] = value.strip()
                save_bulk_fishes(info)
                return render_template('index.html', content=lines, error=None)
            else:
                return render_template('index.html', content=None, error="Este peixe não existe na base de dados.")
        else:
            return render_template('index.html', content=None, error="Resposta inesperada do servidor.")
    else:
        return render_template('index.html', content=None, error="Ocorreu um erro na solicitação.")
    # if response.status_code == 200:
    #         data = response.json()
    #         choices = data["choices"]
    #         if choices:
    #             content = choices[0]["message"]["content"]
    #             lines = content.split(";")
    #             return render_template('index.html', content=lines, error=None)
    #         else:
    #             return render_template('index.html', content=None, error="Este peixe não existe na base de dados.")
    # else:
    #         return render_template('index.html', content=None, error="Ocorreu um erro na solicitação.")

if __name__ == '__main__':
    app.run(debug=True)
