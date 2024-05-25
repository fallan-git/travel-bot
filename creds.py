import json
import time
from datetime import datetime
import requests
from config import IAM_TOKEN_PATH
import logging

def create_new_token():
    url = "http://169.254.169.254/computeMetadata/v1/instance/service-accounts/default/token"
    headers = {
        "Metadata-Flavor": "Google"
    }
    try:
        response = requests.get(url=url, headers=headers, timeout=5)  # Установите таймаут
        if response.status_code == 200:
            token_data = response.json()

            token_data['expires_at'] = time.time() + token_data['expires_in']

            with open(IAM_TOKEN_PATH, "w") as token_file:
                json.dump(token_data, token_file)
            logging.info("Получен новый iam_token")
        else:
            logging.error(f"Ошибка получения iam_token. Статус-код: {response.status_code}")
    except requests.exceptions.ConnectTimeout as e:
        logging.error(f"Ошибка получения iam_token: {e}")
    except Exception as e:
        logging.error(f"Ошибка получения iam_token: {e}")


def get_creds():
    try:
        with open(IAM_TOKEN_PATH, 'r') as f:
            file_data = json.load(f)
            expiration = datetime.strptime(file_data["expires_at"][:26], "%Y-%m-%dT%H:%M:%S.%f")

        if expiration < datetime.now():
            logging.info("Срок годности iam_token истёк")
            create_new_token()
    except:
        create_new_token()

    with open(IAM_TOKEN_PATH, 'r') as f:
        file_data = json.load(f)
        iam_token = file_data["access_token"]


    return iam_token
