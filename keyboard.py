from telebot import types

menu = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
menu1 = types.KeyboardButton('/help📚')
menu2 = types.KeyboardButton('/travel_help🖼')
menu3 = types.KeyboardButton('/town_history🌃')
menu.add(menu1, menu2, menu3)

helpkey = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
help1 = types.KeyboardButton('/support_of_сreators👨‍💻')
help2 = types.KeyboardButton('/travel_help🖼')
help3 = types.KeyboardButton('/town_history🌃')
helpkey.add(help1, help2, help3)