from telebot import types

menu = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
menu1 = types.KeyboardButton('/help')
menu2 = types.KeyboardButton('/support_of_сreators')
menu3 = types.KeyboardButton('/set_town')
menu6 = types.KeyboardButton('/set_country')
menu7 = types.KeyboardButton('/travel_quiz')
menu.add(menu1, menu3,menu6, menu2,  menu7)



helpkey = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
help1 = types.KeyboardButton('/set_town')
help2 = types.KeyboardButton('/set_country')
help3 = types.KeyboardButton('/travel_help')
help4 = types.KeyboardButton('/town_history')
help7 = types.KeyboardButton('/travel_quiz')
help8 = types.KeyboardButton('/interesting_facts')
help6 = types.KeyboardButton('/support_of_creators')
helpkey.add(help1, help2,help7, help4,help3, help6, help8)


travelhelp = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
t1 = types.KeyboardButton('/continue')
t2 = types.KeyboardButton('/menu')


