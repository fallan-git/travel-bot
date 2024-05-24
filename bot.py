import logging
import telebot
import requests
from keyboard import menu, helpkey, token_small
from secret import TOKEN, folder_id
from config import (MAX_GPT_TOKENS, MAX_USER_GPT_TOKENS, MAX_USERS, LOGS, IAM_TOKEN_PATH, TOKENIZE_URL,
                    GPT_MODEL, GPT_URL)
from database import Database
import csv

IAM_TOKEN = 't1.9euelZqencyXy5mLm4mblpXLms2Mxu3rnpWakZOMy8uYk4nJnZPIjovLiZHl8_dQK0JN-e9AMmx1_t3z9xBaP03570AybHX-zef1656VmpnKzp6VioqbnJeVk8qKypSO7_zF656VmpnKzp6VioqbnJeVk8qKypSOveuelZrMkY6Jx8mXx5vOlpiansablrXehpzRnJCSj4qLmtGLmdKckJKPioua0pKai56bnoue0oye.6BLtq5EqCiB5BT0FqIbSDhdBxyo9O8t_izA3_1KPQoroFT0c0R0DXYivpoEI6pftn1LFDMS8QbDOlFTvw4LQBw'

db = Database()

bot = telebot.TeleBot(TOKEN)

logging.basicConfig(filename=LOGS, level=logging.DEBUG,
                    format="%(asctime)s FILE: %(filename)s IN: %(funcName)s MESSAGE: %(message)s", filemode="w")

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    user_name = message.from_user.first_name
    logging.info(f"{user_name} | {chat_id} - новый пользователь")
    db.add_user(chat_id)
    bot.send_message(chat_id,
                     f"<b>Привет {user_name}👋, это бот который поможет тебе в путешествиях.</b>\n\n"
                     f"Для более подробной информации нужно написать /help.\n"
                     f"А для начала взаимодействия с ботом по вашему путешествию напишите /set_town и укажите город.\n",
                     parse_mode='html',reply_markup=menu)

@bot.message_handler(commands=['help'])
def help(message):
    chat_id = message.chat.id
    user_name = message.from_user.first_name
    logging.info(f"{user_name} | {chat_id} - выполнил команду help")
    bot.send_message(chat_id,
                     f"Данный бот 🤖 использует технологии <b>YaGPT</b>.\n\n"
                     f"/support_of_сreators - команда благодаря которой можно получить информацию о создателях бота.\n"
                     f"/travel_help - получить информацию о достопримечательностях города.\n"
                     f"/town_history - узнать историю города\n"
                     f"/set_town - команда для указания нужного вам города, без неё не работают другие команды.\n"
                     f"/get_weather - узнать погоду в городе\n"
                     f"Ограничение по пользователям бота - {MAX_USERS}\n"
                     f"Ограничение токенов для пользователя - {MAX_USER_GPT_TOKENS}\n"
                     f"Ограничение токенов в ответе GPT - {MAX_GPT_TOKENS}\n",
                     parse_mode='html',reply_markup=helpkey)

@bot.message_handler(commands=['support_of_сreators'])
def support_of_сreators(message):
    chat_id = message.chat.id
    user_name = message.from_user.first_name
    logging.info(f"{user_name} | {chat_id} - выполнил команду support_of_сreators")
    bot.send_message(chat_id,
                     f"<b>Эти люди🧑🏼‍💻 работали над ботом, если потребуется помощь, можешь написать кому-то из них:</b>\n\n"
                     f"👨‍🎓<b>Марк</b>\n"
                     f"Discord - <code>lathanael.</code>\n"
                     f"Telegram - ???\n"
                     f"👨‍🎓<b>Алексей</b>\n"
                     f"Discord - <code>noverega10</code>\n"
                     f"Telegram - ???\n"
                     f"🥷<b>Леонид</b>\n"
                     f"Discord - <code>fallan.</code>\n"
                     f"Telegram - <code>@fallangg</code>\n",
                     parse_mode='html',reply_markup=menu)

@bot.message_handler(commands=['set_town'])
def get_town(message):
    chat_id = message.chat.id
    user_name = message.from_user.first_name
    logging.info(f"{user_name} | {chat_id} - выполнил команду set_town")

    bot.send_message(chat_id, 'Напиши <b>город</b>, о котором мы будем говорить в дальнейшем..',
                     parse_mode='html',reply_markup=menu)
    bot.register_next_step_handler(message, check_town_in_csv)

def check_town_in_csv(message):
    with open('city.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        town = message.text
        for row in reader:
            if row["name"] == town:
                return True
    return False

def handle_message(message):
    town = message.text
    chat_id = message.from_user.id
    csv_file = 'city.csv'

    if check_town_in_csv(town, csv_file):
        bot.send_message(chat_id, '<b>Нужный вам город найден в базе данных!</b>😃\nМы сохранили информацию о нём.',
                     parse_mode='html',reply_markup=menu)
        db.update_city(town, chat_id)
    else:
        bot.send_message(chat_id, "<b>Нужный вам город не найден в базе данных!</b>😥\n"
                                  "Напишите команду /travel_help и укажите город заново.",
                     parse_mode='html',reply_markup=menu)
        

@bot.message_handler(commands=['travel_help'])
def get_weather(message):
    chat_id = message.chat.id
    city = db.get_city(chat_id)
    if city == None:
        bot.send_message(chat_id, "<b>Вы не выбрали город, напишите /set_town!</b>😥\n",
                     parse_mode='html',reply_markup=menu)
        return
    PROMPT = [{'role': 'system', 'text': f'Расскажи о главных достопримечательностях в городе под названием '}]
    user_tokens = db.get_tokens(chat_id)
    if user_tokens < 120:
        bot.send_message(chat_id, "<b>У вас нету токенов.</b>😥\n"
                                  "Вам доступны команды: /help, /get_weather и /support_of_сreators",
                     parse_mode='html',reply_markup=token_small)
        return
    success, otvet, tokens_in_answer = ask_gpt(city, PROMPT)
    if success:
        bot.send_message(chat_id, f"<b>{otvet}</b>",
                         parse_mode='html',reply_markup=menu)
        db.update_tokens(tokens_in_answer, chat_id)

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


def ask_gpt(messages, SYSTEM_PROMPT):
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
        "messages": SYSTEM_PROMPT + messages
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



bot.polling()