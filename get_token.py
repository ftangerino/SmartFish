import requests

# Função para enviar uma solicitação GET para a API e receber o token
def receive_token(phone_number):
    url = 'http://localhost:3000/sendToken'
    params = {'phone': phone_number}
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        if 'success' in data and data['success']:
            print("Token enviado com sucesso!")
        else:
            print("Falha ao enviar token.")
    
    except Exception as e:
        print(f"Erro ao enviar solicitação: {e}")

# Número de telefone para o qual o token será enviado
phone_number = '19995978301'  # Substitua pelo número desejado

# Chama a função para receber o token
receive_token(phone_number)