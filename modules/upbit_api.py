import requests
import hashlib
import jwt
import uuid
import time

ACCESS_KEY = "YOUR_ACCESS_KEY"
SECRET_KEY = "YOUR_SECRET_KEY"
SERVER_URL = "https://api.upbit.com"


def get_headers(query=""):
    payload = {
        'access_key': ACCESS_KEY,
        'nonce': str(uuid.uuid4()),
    }

    if query:
        m = hashlib.sha512()
        m.update(query.encode())
        payload['query_hash'] = m.hexdigest()
        payload['query_hash_alg'] = 'SHA512'

    jwt_token = jwt.encode(payload, SECRET_KEY)
    headers = {"Authorization": f"Bearer {jwt_token}"}
    return headers


def get_balance():
    url = f"{SERVER_URL}/v1/accounts"
    headers = get_headers()
    response = requests.get(url, headers=headers)
    return response.json()


def get_ticker(market="KRW-BTC"):
    url = f"{SERVER_URL}/v1/ticker"
    response = requests.get(url, params={"markets": market})
    return response.json()[0]["trade_price"]


def buy_coin(market="KRW-BTC", amount=5000):
    url = f"{SERVER_URL}/v1/orders"
    query = f"market={market}&side=bid&price={amount}&ord_type=price"
    headers = get_headers(query)
    response = requests.post(url, headers=headers, params=query)
    return response.json()


def sell_coin(market="KRW-BTC", volume=0.001):
    url = f"{SERVER_URL}/v1/orders"
    query = f"market={market}&side=ask&volume={volume}&ord_type=market"
    headers = get_headers(query)
    response = requests.post(url, headers=headers, params=query)
    return response.json()
