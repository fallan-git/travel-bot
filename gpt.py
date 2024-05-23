import logging
import requests
from config import (MAX_GPT_TOKENS, MAX_USER_GPT_TOKENS, MAX_USERS, LOGS, IAM_TOKEN_PATH, TOKENIZE_URL,
                    GPT_MODEL, GPT_URL)
from secret import folder_id

IAM_TOKEN = ''

try:
    with open(IAM_TOKEN_PATH, 'r') as file:
        IAM_TOKEN = file.read()
except FileNotFoundError:
    logging.info(f"Файл c IAM_TOKEN не найден.")
except Exception as e:
    logging.info(f"Произошла ошибка при чтении файла: {e}")


def count_gpt_tokens(messages):
    headers = {
        'Authorization': f'Bearer {IAM_TOKEN}',
        'Content-Type': 'application/json'
    }
    data = {
        'modelUri': f"gpt://{folder_id}/yandexgpt-lite",
        "messages": messages
    }
    try:
        response = requests.post(url=TOKENIZE_URL, json=data, headers=headers).json()['tokens']
        return len(response)
    except Exception as e:
        logging.error(e)
        return 0




def ask_gpt(messages, SYSTEM_PROMPT1):
    headers = {
        'Authorization': f'Bearer {IAM_TOKEN}',
        'Content-Type': 'application/json'
    }
    data = {
        'modelUri': f"gpt://{folder_id}/{GPT_MODEL}",
        "completionOptions": {
            "stream": False,
            "temperature": 0.7,
            "maxTokens": 100
        },
        "messages": SYSTEM_PROMPT1 + messages
    }
    try:
        response = requests.post(GPT_URL, headers=headers, json=data)
        if response.status_code != 200:
            return False, f"Ошибка GPT. Статус-код: {response.status_code}", None
        answer = response.json()['result']['alternatives'][0]['message']['text']
        tokens_in_answer = count_gpt_tokens([{'role': 'assistant', 'text': answer}])
        return True, answer, tokens_in_answer
    except Exception as e:
        logging.error(e)
        return False, "Ошибка при обращении к GPT",  None