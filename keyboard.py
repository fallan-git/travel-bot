from telebot import types

menu = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
menu1 = types.KeyboardButton('/help📚')
menu2 = types.KeyboardButton('/support_of_сreators👨‍💻')
menu3 = types.KeyboardButton('/set_town🌃')
menu.add(menu1, menu3, menu2)

helpkey = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
help1 = types.KeyboardButton('/set_town🌃')
help2 = types.KeyboardButton('/support_of_сreators👨‍💻')
help3 = types.KeyboardButton('/travel_help🖼')
help4 = types.KeyboardButton('/town_history🌆')
help5 = types.KeyboardButton('/get_weather🌦')
helpkey.add(help2, help5)
helpkey.add(help1, help3, help4)

token_small = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
token1 = types.KeyboardButton('/support_of_сreators👨‍💻')
token2 = types.KeyboardButton('/get_weather🌦')
token_small.add(token1, token2)
