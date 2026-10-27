import requests
from datetime import datetime

URL_BASE = "https://api.coingecko.com/api/v3"


def buscar_moedas():
    url_moedas = URL_BASE + "/coins/markets"     
    params = {"vs_currency": "usd", "per_page": 10, "page": 1}
    try:
        resposta = requests.get(url_moedas,params= params,timeout = 10)
    except requests.exceptions.ConnectionError as e:
        print(f"Conexao deu erro. Erro: {e}")
        return None
    except requests.exceptions.Timeout as e:
        print(f"Tempo excedido. Erro: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Erro inesperado na requisição. Erro: {e}")
        return None
    if resposta.status_code == 200:
        return resposta.json()
    elif resposta.status_code == 404:
        print("EndPoint nao encontrado.")
        return None
    elif resposta.status_code >= 500:
        print("Erro no servidor da API")
        return None
    else:
        print(f"Status: {resposta.status_code}")
        return None


def buscar_cotacao_dolar():
    url_cotacao_dolar = URL_BASE + "/simple/price"
    params = {"ids": "tether","vs_currencies": "brl"}
    try:
        resposta = requests.get(url_cotacao_dolar, params=params,timeout=10)
    except requests.exceptions.ConnectionError as e:
        print(f"Conexao deu erro. Erro: {e}")
        return None
    except requests.exceptions.Timeout as e:
        print(f"Tempo excedido. Erro: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Erro inesperado na requisição. Erro: {e}")
        return None
    if resposta.status_code == 200:
        dados = resposta.json()
        cotacao = dados["tether"]["brl"]
        return cotacao
    elif resposta.status_code == 404:
        print("EndPoint nao encontrado.")
        return None
    elif resposta.status_code >= 500:
        print("Erro no servidor da API")
        return None
    else:
        print(f"Status: {resposta.status_code}")
        return None


def transformar_moeda(cotacao,moedas):
    moedas_tratadas = []
    for moeda in moedas:
        id_moeda = moeda["id"]
        simbolo = moeda["symbol"].upper()
        nome = moeda["name"]
        preco_usd = moeda["current_price"]
        preco_brl = round(preco_usd * cotacao,2)
        maxima = moeda["high_24h"]
        minima = moeda["low_24h"]
        ranking = moeda["market_cap_rank"]
        variacao_24h = moeda["price_change_percentage_24h"]
        data_atualizacao = datetime.strptime( moeda["last_updated"], "%Y-%m-%dT%H:%M:%S.%fZ")
        if minima is None or maxima is None or minima == 0:
            amplitude = None
            volatilidade = None
        else:
            amplitude = round((maxima - minima) / minima * 100, 2)
            if amplitude < 2:
                volatilidade = "BAIXA"
            elif amplitude <= 5:
                volatilidade = "MEDIA"
            else:
                volatilidade = "ALTA"
        moeda_tratada = {"id_moeda": id_moeda, "simbolo": simbolo, "nome": nome,
                         "preco_usd": preco_usd, "preco_brl": preco_brl,
                         "amplitude": amplitude, "volatilidade": volatilidade,
                         "ranking": ranking, "variacao_24h": variacao_24h,
                         "data_atualizacao": data_atualizacao}
        moedas_tratadas.append(moeda_tratada)
    return moedas_tratadas



moedas = buscar_moedas()
cotacao = buscar_cotacao_dolar()
resultado = transformar_moeda(cotacao,moedas)
print(resultado[0])
