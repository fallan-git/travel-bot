from telebot import types

menu = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
menu1 = types.KeyboardButton("/help")
menu2 = types.KeyboardButton("/support")
menu3 = types.KeyboardButton("/set_town")
menu6 = types.KeyboardButton("/set_country")
menu7 = types.KeyboardButton("/travel_quiz")
menu8 = types.KeyboardButton("/weather")
menu.add(menu1, menu3, menu6, menu2,  menu7, menu8)

helpkey = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
help1 = types.KeyboardButton("/set_town")
help2 = types.KeyboardButton("/set_country")
help3 = types.KeyboardButton("/travel_help")
help4 = types.KeyboardButton("/town_history")
help7 = types.KeyboardButton("/travel_quiz")
help8 = types.KeyboardButton("/interesting_facts")
help9 = types.KeyboardButton("/city_restaurants")
help10 = types.KeyboardButton("/weather")
help6 = types.KeyboardButton("/support")
helpkey.add(help1, help2, help7, help4, help3, help6, help8, help9, help10)

travelhelp = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
t2 = types.KeyboardButton('/menu')
travelhelp.add(t2)


