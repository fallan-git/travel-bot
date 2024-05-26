from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, Message
from keyboard import menu, helpkey, travelhelp
import random
from super_secret import TOKEN
from config import (MAX_GPT_TOKENS, MAX_USER_GPT_TOKENS, MAX_USERS)
from database import Database
from yandexgpt import ask_gpt
from geopy.geocoders import Nominatim
import requests

bot = TeleBot(TOKEN)
db = Database()
#######################################################DatabaseFunction#########################################################
def check_number_of_users(chat_id):
    count = db.count_users(chat_id)
    if count is None:
        return None, "Ошибка при работе с БД"
    if count > MAX_USERS:
        return None, "Превышено максимальное количество пользователей"
    return True, ""


######################################################MainFunctions#########################################################

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    user_name = message.from_user.first_name
    db.add_user(chat_id)
    bot.send_message(chat_id,
                     f"<b>Привет {user_name}👋, Я Форд Префект. Планета Земля оказалась самой интересной в моем путешествии по галактике, я был во всех городах и странах Земли, скажу больше, я был почти во всех галактиках. Если вы читали книгу Автостопом по галактике, то вы точно меня помните!\n Если вы собрались в путешествие, то обязательно пишите мне и я расскажу очень многое о городе, его достопримечательностях и ресторанах. </b>\n\n"
                     f"Для более подробной информации нужно написать /help.\n"
                     f"Команда /menu переведет вас в режим со всеми комнадами бота. "
                     f"Команда /weather покажет вам погоду в вашем городе\n"
                     f"А для начала взаимодействия со мной по вашему путешествию напишите /set_town и укажите город, также вам следует узаать интересующую вас страну через команду /set_country. Затем вам станет доступны другие команды. "
                     f"Я любитель разных викторин и я составил викторину про разные города мира, правильный ответ - +2 балла вам и возможность воспользоваться командой /interesting_facts\n",
                     parse_mode='html',reply_markup=helpkey)

@bot.message_handler(commands=['help'])
def help(message):
    chat_id = message.chat.id

    bot.send_message(chat_id,
                     f"Чтобы общатсья со мной, вы должны использовать эти команды.\n\n"
                     f" /weather - Команда для получения погоды в городе пользователя"
                     f" /support_of_creators - Команда, благодаря которой можно получить информацию о создателях бота. \n"
                     f" /travel_quiz - Команда для начала викторины по разным городам мира. \n"
                     f" /travel_help - Получить информацию о достопримечательностях города. \n"
                     f" /town_history - Узнать историю города\n "
                     f" /set_town - Команда для указания нужного вам города, без неё не работают другие команды. \n"
                     f" /set_country - Команда для указания интересующей вас страны, без неё не работают другие команды. \n"
                     f" /interesting_facts - 9 Интересных фактов о стране пользователя,\n команда работает, если пользователь имеет не меньше 2 баллов в викторине. \n За 1 пропуск к команде берется 2 балла"
                     f"Когда я попал на Землю, Верховный суд запретил мне общаться со всеми землянами про мои путешествия, из-за этого я могу делиться этим только с  {MAX_USERS} пользователями бота\n"
                     f"Также я не могу рассказать слишком много, поэтому когда мы пройдем рубеж 4000 токенов(1 токен = +-3 символам), мне придется перестать говрить.\n"
                     f"Ограничение токенов в ответе  - {MAX_GPT_TOKENS}\n",
                     parse_mode='html', reply_markup=helpkey)

@bot.message_handler(commands=['support'])
def support(message):
    chat_id = message.chat.id
    bot.send_message(chat_id,
                     f"<b>Эти люди🧑🏼‍💻 работали над ботом, если потребуется помощь, можешь написать кому-то из них:</b>\n\n"
                     f"👨‍🎓<b>Марк</b>\n"
                     f"Discord - <code>lathanael.</code>\n"
                     f"Telegram - @Ts_Mark1\n"
                     f"👨‍🎓<b>Алексей</b>\n"
                     f"Discord - <code>noverega10</code>\n"
                     f"Telegram - @noverega\n"
                     f"🥷<b>Леонид</b>\n"
                     f"Discord - <code>fallan.</code>\n"
                     f"Telegram - <code>@fallangg</code>\n",
                     parse_mode='html')

@bot.message_handler(commands=['menu'])
def menu(message):
    bot.send_message(message.chat.id, 'Перевожу в меню...', reply_markup=helpkey)


#####################################################GetParamsModule##########################################################

@bot.message_handler(commands=['set_town'])
def get_town(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Напиши <b>город</b>, о котором мы будем говорить в дальнейшем..',
                     parse_mode='html')
    bot.register_next_step_handler(message, handle_message)

@bot.message_handler(commands=['set_country'])
def start_country(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Напиши <b>интересующую страну</b>, о котором мы будем говорить в дальнейшем..',
                     parse_mode='html')
    bot.register_next_step_handler(message, set_country)


####################################################GenerationModule###########################################################
@bot.message_handler(commands=['city_restaurants'])
def city_restaurants(message):
    chat_id = message.chat.id

    status_check_users, error_message = check_number_of_users(chat_id)
    if not status_check_users:
        bot.send_message(chat_id, error_message)
        return

    city = db.get_city(chat_id)
    if city == None:
        bot.send_message(chat_id, "<b>Вы не выбрали город, напишите /set_town!</b>😥\n",
                         parse_mode='html', reply_markup=menu)
        return
    bot.send_message(chat_id, f'Выбранный город: {city}.\n Начинается генерация...')

    PROMPT = [{'role': 'system',
               'text': f'Расскажи подробно про самые популярные и интересные рестораны в городе {city}, Рассказ должен быть не менее чем в 1000 символов, тебе нужно уложиться в 1000 символов. В конце сделай завершающее предложение, не пиши никакой поясняющий текст от себя.'}]
    user_tokens = db.get_tokens(chat_id)
    if user_tokens < 200:
        bot.send_message(chat_id, "<b>У вас нету токенов.</b>😥\n"
                                  "Вам доступны команды: /help, /get_weather и /support_of_сreators",
                         parse_mode='html', reply_markup=menu)
        return
    success, otvet, tokens_in_answer = ask_gpt(PROMPT)
    if success:
        bot.send_message(chat_id, f"<b>{otvet}</b>",
                         parse_mode='html', reply_markup=helpkey)
        db.update_history(otvet, chat_id)
        db.update_tokens(tokens_in_answer, chat_id)
@bot.message_handler(commands=['interesting_facts'])
def facts(message):
    chat_id = message.chat.id

    status_check_users, error_message = check_number_of_users(chat_id)
    if not status_check_users:
        bot.send_message(chat_id, error_message)
        return

    score = db.get_score(chat_id)
    if score < 2:
        bot.send_message(chat_id, 'Как вы помните, у этой команды есть оплата - 2 Балла, \n'
                                  f'Кол-во баллов: {score}\n'
                                  f'Чтобы заработать баллы вам нужно поучаствовать в викторине  и ответить хотя бы 1 раз правильно.\n Чтобы начать викторину нажмите /travel_quiz', reply_markup=helpkey)
        return
    country = db.get_country(chat_id)
    if country == None:
        bot.send_message(chat_id, "<b>Вы не выбрали страну, напишите /set_country!</b>😥\n",
                         parse_mode='html', reply_markup=menu)
        return
    bot.send_message(chat_id, f'Выбранная страна: {country}.\n Начинается генерация интересных фактов...')

    PROMPT = [{'role': 'system',
               'text': f'Расскажи 9 самых интересных фактов про страну {country}Ты должен сделать текст не более чем на 900 символов. Сделай завершающий интересный факт, не пиши никакой поясняющий текст от себя.'}]
    user_tokens = db.get_tokens(chat_id)
    if user_tokens < 200:
        bot.send_message(chat_id, "<b>У вас нету токенов.</b>😥\n"
                                  "Вам доступны команды: /help, /get_weather и /support_of_сreators, /travel_quiz",
                         parse_mode='html', reply_markup=menu)
        return
    success, otvet, tokens_in_answer = ask_gpt(PROMPT)
    if success:
        bot.send_message(chat_id, f"<b>{otvet}</b>",
                         parse_mode='html', reply_markup=helpkey)
        db.update_tokens(tokens_in_answer, chat_id)
        db.update_score(score-2, chat_id)
@bot.message_handler(commands=['town_history'])
def city_history(message):
    chat_id = message.chat.id

    status_check_users, error_message = check_number_of_users(chat_id)
    if not status_check_users:
        bot.send_message(chat_id, error_message)
        return

    city = db.get_city(chat_id)
    if city == None:
        bot.send_message(chat_id, "<b>Вы не выбрали город, напишите /set_town!</b>😥\n",
                     parse_mode='html',reply_markup=menu)
        return
    bot.send_message(chat_id, f'Выбранный город: {city}.\n Начинается генерация истории...')

    PROMPT = [{'role': 'system', 'text': f'Расскажи историю города под названием {city}. Напиши подробный рассказ не более чем на 900 символов. В конце сделай завершающее предложение, не пиши никакой поясняющий текст от себя.'}]
    user_tokens = db.get_tokens(chat_id)
    if user_tokens < 200:
        bot.send_message(chat_id, "<b>У вас нету токенов.</b>😥\n"
                                  "Вам доступны команды: /help, /get_weather и /support_of_сreators",
                     parse_mode='html',reply_markup=menu)
        return
    success, otvet, tokens_in_answer = ask_gpt(PROMPT)
    if success:
        bot.send_message(chat_id, f"<b>{otvet}</b>",
                         parse_mode='html',reply_markup=helpkey)
        db.update_history(otvet, chat_id)
        db.update_tokens(tokens_in_answer, chat_id)
@bot.message_handler(commands=['travel_help'])
def travel_help(message):
    chat_id = message.chat.id

    status_check_users, error_message = check_number_of_users(chat_id)
    if not status_check_users:
        bot.send_message(chat_id, error_message)
        return

    city = db.get_city(chat_id)
    if city == None:
        bot.send_message(chat_id, "<b>Вы не выбрали город, напишите /set_town!</b>😥\n",
                     parse_mode='html', reply_markup=menu)
        return
    bot.send_message(chat_id, f'Выбранный город: {city}')

    PROMPT = [{'role': 'system', 'text': f'Ты опытный путешественник и был во всех городах мира. Не пиши никакой поясняющий текст от себя. Продолжи подробный рассказ про достопримечательности города {city} Расскажи подробно про самые интерессные и доступные достопримечательности города {city}. В конце сделай завершающее предложение, не пиши никакой поясняющий текст от себя. Сделай текст не более чем на 900 символов'}]
    user_tokens = db.get_tokens(chat_id)
    if user_tokens < 200:
        bot.send_message(chat_id, "<b>У вас нету токенов.</b>😥\n"
                                  "Вам доступны команды: /help, /get_weather и /support_of_сreators",
                     parse_mode='html', reply_markup=menu)
        return
    success, otvet, tokens_in_answer = ask_gpt(PROMPT)
    if success:
        bot.send_message(chat_id, f"<b>{otvet}</b>",
                         parse_mode='html', reply_markup=travelhelp)
        db.update_answer(otvet, chat_id)
        db.update_tokens(tokens_in_answer, chat_id)

@bot.message_handler(commands=['weather'])
def get_weather(message):
    user_id = message.from_user.id
    msg = bot.send_message(user_id, 'Напиши город, на который хочешь узнать погоду')
    bot.register_next_step_handler(msg, weather)
def weather(message):
    api_key = '621832e1e20c2758886536204ce51448'
    city = message.text
    base_url = 'http://api.openweathermap.org/data/2.5/weather?'
    geolocator = Nominatim(user_agent="my_app")
    location = geolocator.geocode(city)
    lon = str(location.longitude)
    lat = str(location.latitude)

    complete_url = f"{base_url}lat={lat}&lon={lon}&exclude=hourly,daily&appid={api_key}"
    response = requests.get(complete_url)
    if response.status_code == 200:
        data = response.json()
        if 'main' in data and 'weather' in data:
            main = data['main']
            weather = data['weather']
            temperature = (main['temp'] * 0.1) // 2
            pressure = main['pressure']
            humidity = main['humidity']
            bot.send_message(message.from_user.id, f'Погода в городе {city} на ближайшее время: Температура: {temperature}+-5 градусов, Давление: {pressure}Мбар, Влажность: {humidity}')

####################################################FunctionsModule##########################################################
def set_country(message):
    chat_id = message.chat.id
    country = message.text
    town = db.get_city(chat_id)
    user_name = message.from_user.first_name
    tokens = db.get_tokens(chat_id)
    score = db.get_score(chat_id)
    if town in ['/set_town', '/travel_help', '/town_history', '/help', '/support_of_creators', '/set_country',
                '/interesting_facts']:
        bot.send_message(chat_id, 'При обработки этой команды вам стоит написать страну. /set_country', reply_markup=menu)
        return
    else:
        db.update_country(country, chat_id)
        bot.send_message(chat_id, f'Вы успешно обновили страну!\n'
                                  f'Ваша анкета:\n'
                                  f'Имя: {user_name}\n'
                                  f'Чат_айди: {chat_id}\n'
                                  f'Город: {town}\n'
                                  f'Кол-во токенов: {tokens}\n'
                                  f'Интересующая страна: {country}\n'
                                  f'Кол-во баллов: {score}', reply_markup=helpkey)
        return
def handle_message(message):
    town = message.text
    user_name = message.from_user.first_name
    chat_id = message.chat.id
    tokens = db.get_tokens(chat_id)
    score = db.get_score(chat_id)
    country = db.get_country(chat_id)
    if town in ['/set_town', '/travel_help', '/town_history', '/help', '/support_of_creators', '/set_country', '/interesting_facts']:
        bot.send_message(chat_id, 'При обработки этой команды вам стоит написать город. /set_town', reply_markup=menu)
        return
    else:
        db.update_city(town, chat_id)
        bot.send_message(chat_id, f'Вы успешно обновили город!\n'
                                  f'Ваша анкета:\n'
                                  f'Имя: {user_name}\n'
                                  f'Чат_айди: {chat_id}\n'
                                  f'Город: {town}\n'
                                  f'Кол-во токенов: {tokens}\n'
                                  f'Интересующая страна: {country}\n'
                                  f'Кол-во баллов: {score}', reply_markup=helpkey)
        return

###################################################TravelQuizModule#########################################################

questions = {
    "Какой город называют Большим яблоком?": ["Нью-Йорк", "Лос-Анджелес", "Токио"],
    "В каком городе находится Эйфелева башня?": ["Париж", "Лондон", "Рим"],
    "Столицей какой страны является Берлин?": ["Германия", "Франция", "Италия"],
    "В каком городе расположен Колизей?": ["Рим", "Афины", "Каир"],
    "Какой город называют Городом мостов?": ["Венеция", "Амстердам", "Прага"],
    "В каком городе находится статуя Христа-Искупителя?": ["Рио-де-Жанейро", "Буэнос-Айрес", "Лима"],
    "Столицей какой страны является Москва?": ["Россия", "Украина", "Беларусь"],
    "В каком городе находится самая высокая гора в мире?": ["Катманду", "Пекин", "Дели"],
    "Какой город называют Городом каналов?": ["Амстердам", "Венеция", "Брюгге"],
    "В каком городе расположен Букингемский дворец?": ["Лондон", "Париж", "Мадрид"],
    "Какой город является крупнейшим по площади в мире?": ["Нью-Йорк", "Токио", "Шанхай"],
    "Какой город называют Городом ветров?": ["Чикаго", "Лондон", "Париж"],
    "В каком городе находится самый большой музей в мире?": ["Париж", "Лондон", "Вашингтон"],
    "Какой город является столицей самой маленькой страны в мире?": ["Ватикан", "Монако", "Сан-Марино"],
    "В каком городе находится самая высокая башня в мире?": ["Дубай", "Токио", "Шанхай"],
    "Какой город называют Городом ангелов?": ["Лос-Анджелес", "Париж", "Лондон"],
    "В каком городе находится самая большая площадь в мире?": ["Пекин", "Москва", "Токио"],
    "Какой город является самым густонаселенным в мире?": ["Токио", "Шанхай", "Дели"],
    "В каком городе находится самый старый университет в мире?": ["Оксфорд", "Кембридж", "Болонья"],
    "Какой город называют Городом семи холмов?": ["Рим", "Стамбул", "Лиссабон"],
    "В каком городе находится самый большой порт в мире?": ["Шанхай", "Сингапур", "Дубай"],
    "Какой город называют Восточной Венецией?": ["Сучжоу", "Венеция", "Амстердам"],
    "В каком городе находится самый большой аквариум в мире?": ["Атланта", "Дубай", "Токио"],
    "Какой город называют Городом тысячи храмов?": ["Киото", "Бангкок", "Львов"],
    "В каком городе находится самый большой небоскреб в мире?": ["Дубай", "Шанхай", "Токио"],
    "Какой город называют Городом музыки?": ["Вена", "Париж", "Нью-Йорк"],
    "В каком городе находится самая большая библиотека в мире?": ["Вашингтон", "Париж", "Лондон"],
    "Какой город называют Городом огней?": ["Париж", "Лас-Вегас", "Дубай"],
    "В каком городе находится самый большой парк в мире?": ["Нью-Йорк", "Лондон", "Токио"],
    "Какой город называют Городом любви?": ["Париж", "Вена", "Рим"],
    "В каком городе находится самый большой стадион в мире?": ["Пхеньян", "Барселона", "Лондон"],
    "Какой город называют Городом небоскребов?": ["Нью-Йорк", "Токио", "Дубай"],
    "В каком городе находится самый большой торговый центр в мире?": ["Дубай", "Пекин", "Шанхай"],
    "Какой город называют Городом контрастов?": ["Мумбаи", "Рио-де-Жанейро", "Стамбул"],
    "В каком городе находится самый большой океанариум в мире?": ["Атланта", "Дубай", "Токио"],
    "Какой город называют Городом культуры?": ["Париж", "Лондон", "Вена"],
    "В каком городе находится самый большой музей современного искусства в мире?": ["Нью-Йорк", "Париж", "Лондон"],
    "Какой город называют Городом вечной весны?": ["Куньмин", "Мехико", "Мадрид"],
    "В каком городе находится самая длинная улица в мире?": ["Торонто", "Лондон", "Париж"],
    "Какой город называют Городом моды?": ["Париж", "Милан", "Лондон"],
    "В каком городе находится самый большой зоопарк в мире?": ["Сан-Диего", "Лондон", "Пекин"],
    "Какой город называют Городом технологий?": ["Токио", "Сан-Франциско", "Шанхай"],
    "В каком городе находится самый большой ботанический сад в мире?": ["Лондон", "Париж", "Берлин"],
    "Какой город называют Городом музеев?": ["Париж", "Лондон", "Вашингтон"],
    "В каком городе находится самое большое колесо обозрения в мире?": ["Дубай", "Лондон", "Лас-Вегас"],
    "Какой город называют Городом искусства?": ["Флоренция", "Париж", "Вена"],
    "В каком городе находится самый большой тематический парк в мире?": ["Орландо", "Токио", "Шанхай"],
    "Какой город называют Городом истории?": ["Рим", "Стамбул", "Афины"],
    "В каком городе находится самый большой океанариум в мире?": ["Атланта", "Дубай", "Токио"],
    "Какой город называют Городом фестивалей?": ["Эдинбург", "Рио-де-Жанейро", "Ноттинг-Хилл"],
    "В каком городе находится самый большой аквапарк в мире?": ["Дубай", "Орландо", "Токио"],
    "Какой город называют Городом пляжей?": ["Рио-де-Жанейро", "Майами", "Барселона"],
    "В каком городе находится самый большой парк развлечений в мире?": ["Орландо", "Париж", "Токио"],
    "Какой город называют Городом гор?": ["Кейптаун", "Рио-де-Жанейро", "Сан-Франциско"],
    "В каком городе находится самая высокая гора в мире?": ["Катманду", "Пекин", "Дели"],
    "Какой город называют Городом дождей?": ["Лондон", "Сиэтл", "Ванкувер"],
    "В каком городе находится самый большой водопад в мире?": ["Виктория", "Ниагарский", "Игуасу"],
    "Какой город называют Городом туманов?": ["Сан-Франциско", "Лондон", "Амстердам"],
    "В каком городе находится самая длинная река в мире?": ["Каир", "Хартум", "Асуан"],
    "Какой город называют Городом пустынь?": ["Дубай", "Каир", "Лас-Вегас"],
    "В каком городе находится самый большой лес в мире?": ["Амазонка", "Конго", "Тайга"],
    "Какой город называют Городом джунглей?": ["Рио-де-Жанейро", "Киншаса", "Манаус"],
    "В каком городе находится самый большой остров в мире?": ["Гренландия", "Мадагаскар", "Новая Гвинея"],
    "Какой город называют Городом вулканов?": ["Неаполь", "Киото", "Портленд"],
    "В каком городе находится самый большой гейзер в мире?": ["Йеллоустоун", "Долина гейзеров", "Исландия"],
    "Какой город называют Городом гейзеров?": ["Долина гейзеров", "Йеллоустоун", "Исландия"]
}

def generate_quiz():
    # Выбрать случайный вопрос
    question = random.choice(list(questions.keys()))
    # Получить варианты ответов
    answers = questions[question]

    return question, answers


def check_answer(question, text):
    correct_answer = questions[question][0]
    return text == correct_answer

@bot.message_handler(commands=['travel_quiz'])
def start_quiz(message):
    global question
    chat_id = message.chat.id
    # Отправить приветственное сообщение
    bot.send_message(chat_id, text="Давай поиграем в викторину про города мира.")

    # Сгенерировать первый вопрос
    question, answers = generate_quiz()

    # Отправить вопрос и варианты ответов
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    bot.send_message(chat_id, f"Давай поиграем в викторину про города мира. Вопрос: {question}")
    for answer in answers:
        keyboard.add(KeyboardButton(answer))
    bot.send_message(chat_id,'Ваш ответ: ', reply_markup=keyboard)
    bot.register_next_step_handler(message, handle_message_for_quiz)

def handle_message_for_quiz(message):
    chat_id = message.chat.id
    score = db.get_score(chat_id)
    text = message.text


    if text in questions[question]:
        correct = check_answer(question, text)

        if correct:
            bot.send_message(chat_id, text="Правильно! Сыграем снова?\n Для нового вопроса нажми /travel_quiz", reply_markup=helpkey)
            db.update_score(score+2, chat_id)
        else:
            bot.send_message(chat_id, f"Неправильно. Правильный ответ: {questions[question][0]}.  Сыграем снова?\n Для нового вопроса нажми /travel_quiz", reply_markup=helpkey)

    else:
        bot.send_message(chat_id, text="Пожалуйста, ответьте на вопрос, выбрав один из вариантов.")


bot.polling()