import requests
import time
import json
import re
from urllib.error import HTTPError

# GLOBAL access token. getter function below.
ACCESS_TOKEN = None
def validateAccessToken(token):
    headers = {}
    headers['Authorization'] = f"token {token}"
    res = requests.get("https://api.github.com/rate_limit", headers=headers)

    return res.status_code != 401

def writeAccessToken(token):
    with open('./config/access_token.json', 'w') as config_file:
        data = {}
        data['access_token'] = token or "<YOUR_GITHUB_PERSONAL_ACCESS_TOKEN>"
        json.dump(data, config_file)

def loadAccessToken():
    with open('./config/access_token.json') as config_file:
        data = json.load(config_file)
        global ACCESS_TOKEN
        ACCESS_TOKEN = data['access_token']

def getAccessToken():
    return ACCESS_TOKEN