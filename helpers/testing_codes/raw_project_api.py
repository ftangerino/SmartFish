import requests
import json

response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": "Bearer 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",
        # "HTTP-Referer": f"{YOUR_SITE_URL}", # Optional, for including your app on openrouter.ai rankings.
        # "X-Title": f"{YOUR_APP_NAME}", # Optional. Shows in rankings on openrouter.ai.
    },
    data=json.dumps({
        "model": "mistralai/mixtral-8x7b-instruct", # Optional
        "messages": [
            {"role": "user", "content": "What is the meaning of life?"}
        ],
        "top_p": 1,
        "temperature": 0.8,
        "frequency_penalty": 0.1,
        "presence_penalty": 0,
        "repetition_penalty": 1,
        "top_k": 1,
    })
)

# Verifique se a solicitação foi bem-sucedida (código de status 200)
if response.status_code == 200:
    # A resposta geralmente é um JSON, então você pode decodificá-la usando o método json()
    data = response.json()
    print(data)
else:
    print("Ocorreu um erro na solicitação. Código de status:", response.status_code)
