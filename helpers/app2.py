from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__)

# Lista de peixes pré-configurados
peixes_aquario = [
    "Guppy",
    "Tetra-neon",
    "Molly",
    "Betta",
    "Acará-disco",
    "Peixe-palhaço",
    "Ancistrus",
    "Danio-zebra",
    "Peixe-espada",
    "Barbo tigre",
    "Ramirezi",
    "Carpa koi",
    "Ciclídeo-frontosa",
    "Tetra fantasma negro",
    "Bandeira vermelha",
    "Peixe-borboleta",
    "Tetra-serpae",
    "Molinésia",
    "Killifish",
    "Peixe-gato de vidro",
    "Tetra limão",
    "Cascalho",
    "Ciclídeo-labido",
    "Tetra neon negro",
    "Gourami-anão",
    "Tetra colombiano",
    "Peixe-arco-íris australiano",
    "Tetra de rummy",
    "Rasbora harlequin",
    "Acará-bandeira",
    "Barbos-cereja",
    "Peixe-borboleta africano",
    "Botia palhaço",
    "Ciclídeo-borboleta",
    "Tetra-cardinal",
    "Platy",
    "Tetra ouro",
    "Cabeça de leão",
    "Rasbora galaxy",
    "Tetra diamante"
]

@app.route('/')
def index():
    return render_template('index.html', peixes_aquario=peixes_aquario)

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
                "content": "You will provide information about fish that the user enters. You always need to provide a short sentence about the fish, the amount of food it eats, pH of water, and how often it should be fed (provide these pieces of information separately), always provide quantity and period in numbers such as weight (not in percentage of weight but in grams that he should consume, if you don't know how to do the conversion), pH of water, and hours. If the provided fish doesn't consume food, add the type of food it consumes. If you don't know, answer that this fish doesn't exist in the database. If the fish is not suitable for farming in an aquarium, just send a notification back to the user stating this and ignore all the rest of the instructions. Always answer in portuguese (pt-br). "
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
            lines = content.split(".")
            return render_template('index.html', content=lines, error=None, peixes_aquario=peixes_aquario)
        else:
            return render_template('index.html', content=None, error="Este peixe não existe na base de dados.", peixes_aquario=peixes_aquario)
    else:
        return render_template('index.html', content=None, error="Ocorreu um erro na solicitação.", peixes_aquario=peixes_aquario)

@app.route('/search_fish', methods=['POST'])
def search_fish():
    search_query = request.form['search_query'].lower()
    search_results = [peixe for peixe in peixes_aquario if search_query in peixe.lower()]
    return render_template('index.html', peixes_aquario=search_results)

if __name__ == '__main__':
    app.run(debug=True)
