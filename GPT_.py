import requests
import logging
import Config_
from Config_ import SYSTEM_PROMPT1, IAM_TOKEN, FOLDER_ID, TOKENIZE_URL, GPT_MODEL, GPT_URL
import csv
import telebot


@bot.message_handler(commands=['get_town'])
def get_town(message):
    user_id = message.from_user.id
    bot.send_message(user_id, 'Напиши город, о достопримечательностях которого ты хочешь услышать.')
    bot.register_next_step_handler(message, check_town_in_csv)

def check_town_in_csv(message):
    with open('worldcities.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        town = message.text
        for row in reader:
            if row["city_ascii"] == town:
                return True
    return False


def handle_message(message):
    town = message.text
    user_id = message.from_user.id
    csv_file = 'worldcities.csv'

    if check_town_in_csv(town, csv_file):
        bot.send_message(user_id, 'Нужный вам город найден в Базе данных:>')
    else:
        bot.send_message(user_id, "Нужный вам город не найден в Базе данных:(")

@bot.message_handler(commands=['get_weather'])
def get_weather(message):
    user_id = message.from_user.id
    Config_.SYSTEM_PROMPT1 = [{'role': 'system', 'text': f'Расскажи о погоде на ближайшую неделю в городе под названием town '}]



def count_gpt_tokens(messages):
    headers = {
        'Authorization': f'Bearer {IAM_TOKEN}',
        'Content-Type': 'application/json'
    }
    data = {
        'modelUri': f"gpt://{FOLDER_ID}/yandexgpt-lite",
        "messages": messages
    }
    try:
        response = requests.post(url=TOKENIZE_URL, json=data, headers=headers).json()['tokens']
        return len(response)
    except Exception as e:
        logging.error(e)
        return 0


def ask_gpt(messages):
    headers = {
        'Authorization': f'Bearer {IAM_TOKEN}',
        'Content-Type': 'application/json'
    }
    data = {
        'modelUri': f"gpt://{FOLDER_ID}/{GPT_MODEL}",
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

