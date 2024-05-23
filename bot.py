import logging
import telebot
from keyboard import menu, helpkey
from secret import TOKEN
from config import MAX_GPT_TOKENS, MAX_USER_GPT_TOKENS, MAX_USERS, LOGS
from database import Database
from gpt import ask_gpt
import csv

db = Database()
db.create_database()

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
                     f"А для начала взаимодействия с ботом по вашему путешествию напишите /travel_help.\n",
                     parse_mode='html',reply_markup=menu)

@bot.message_handler(commands=['help'])
def help(message):
    chat_id = message.chat.id
    user_name = message.from_user.first_name
    logging.info(f"{user_name} | {chat_id} - выполнил команду help")
    bot.send_message(chat_id,
                     f"Данный бот 🤖 использует технологии <b>YaGPT</b>.\n\n"
                     f"/support_of_сreators - команда благодаря которой можно получить информацию о создателях бота.\n"
                     f"/travel_help - получить информацию о достопримечательностях города и о том как сегодня одеться.\n"
                     f"/town_history - узнать историю города\n\n"
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

@bot.message_handler(commands=['travel_help'])
def get_town(message):
    chat_id = message.from_user.id
    user_name = message.from_user.first_name
    logging.info(f"{user_name} | {chat_id} - выполнил команду travel_help")

    bot.send_message(chat_id, 'Напиши <b>город</b>, о достопримечательностях 🏛 которого ты хочешь услышать.',
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
        
        
@bot.message_handler(commands=['get_weather'])
def get_weather(message):
    user_id = message.from_user.id
    SYSTEM_PROMPT1 = [{'role': 'system', 'text': f'Расскажи о погоде на ближайшую неделю в городе под названием town '}]
    ask_gpt(message, SYSTEM_PROMPT1)

bot.polling()
