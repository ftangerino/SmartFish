import requests

def send_token(phone):
    try:
        response = requests.get(f"http://localhost:3000/sendToken?phone={phone}")
        response.raise_for_status()  # Lançar exceção se a solicitação falhar
        print("Token enviado com sucesso")
    except Exception as err:
        print(f"Erro ao enviar token: {err}")
        # Aqui você pode adicionar lógica adicional de tratamento de erro, se necessário

# Exemplo de uso
if __name__ == "__main__":
    phone_number = input("Digite o número de telefone para enviar o token: ")
    send_token(phone_number)