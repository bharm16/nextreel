import requests
import json

from tmdbsimple.createSession import request_token

API_KEY = '1ce9398920594a5521f0d53e9b33c52f'


def generate_request_token(api_key):
    response = requests.get('https://api.themoviedb.org/3/authentication/token/new', params={'api_key': api_key})
    data = response.json()
    return data['request_token']


def validate_with_login(api_key, request_token, username, password):
    url = "https://api.themoviedb.org/3/authentication/token/validate_with_login"
    payload = {
        "username": username,
        "password": password,
        "request_token": request_token
    }
    headers = {
        "content-type": "application/json",
    }
    params = {"api_key": api_key}
    response = requests.post(url, headers=headers, params=params, data=json.dumps(payload))
    return response.status_code == 200


def create_session_id(api_key, request_token):
    url = "https://api.themoviedb.org/3/authentication/session/new"
    payload = {"request_token": request_token}
    params = {"api_key": api_key}
    response = requests.post(url, params=params, data=json.dumps(payload))
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        data = response.json()
        return data


REQUEST_TOKEN = generate_request_token(API_KEY)
print(request_token)
VALID_LOGIN = validate_with_login(API_KEY, REQUEST_TOKEN, "bharm01", "dogtej-xapqeB-gyqvo7")

if VALID_LOGIN:
    session_id = create_session_id(API_KEY, REQUEST_TOKEN)
    print("Session ID: ", session_id)
else:
    print("Failed to validate login.")
