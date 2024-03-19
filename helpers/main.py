import requests
import json

response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": "Bearer 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",
        # "HTTP-Referer": f"{YOUR_SITE_URL}", # Optional, for including your app on openrouter.ai rankings.
        # "X-Title": f"{YOUR_APP_NAME}", # Optional. Shows in rankings on openrouter.ai.
    },
#     data=json.dumps({
#         "model": "mistralai/mixtral-8x7b-instruct", # Optional
#         "messages": [
#             {"role": "user", "content": "What is the meaning of life?"}
#         ]
#     })
# )



  data=json.dumps({
    "model": "mistralai/mixtral-8x7b-instruct", # Optional
    "messages": [
        {
          "role": "system", 
          "content": "You will provide information about fish that the user enters. You always need to provide a short sentence about the fish, the amount of food it eats, pH of water, and how often it should be fed (provide these pieces of information separately), always provide quantity and period in numbers such as weight (not in percentage of weight but in grams that he should consume, if you don't know how to do the conversion), pH of water, and hours. If the provided fish doesn't consume food, add the type of food it consumes. If you don't know, answer that this fish doesn't exist in the database. Always answer in portuguese (pt-br)."
        },
        {
          "role": "user", 
          "content": "preciso de informações acerca do peixe palhaço"
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
        # Dividir o conteúdo em linhas sempre que houver um ponto
        lines = content.split(".")
        # Imprimir cada linha
        for line in lines:
            print(line.strip())  # Remover espaços em branco adicionais
    else:
        print("Não há escolhas disponíveis na resposta.")
else:
    print("Ocorreu um erro na solicitação. Código de status:", response.status_code)