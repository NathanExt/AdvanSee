import requests

def notebook():
    url = 'https://sensedia.uisa.com.br/app-equipment/api/v1/firebase/get?environment=prd&type=notebook'

    try:
        response = requests.get(url)
        response.raise_for_status()  # lança exceção para status 4xx/5xx

        dados = response.json()
        if isinstance(dados, list):
            return dados
        else:
            print("Resposta não é uma lista:", type(dados))
            return []

    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")
        return []

def desktop():
    url = 'https://sensedia.uisa.com.br/app-equipment/api/v1/firebase/get?environment=prd&type=desktop'

    try:
        response = requests.get(url)
        response.raise_for_status()  # lança exceção para status 4xx/5xx

        dados = response.json()
        if isinstance(dados, list):
            return dados
        else:
            print("Resposta não é uma lista:", type(dados))
            return []

    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")
        return []
