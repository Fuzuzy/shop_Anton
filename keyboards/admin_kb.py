from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

button_load = KeyboardButton('Загрузить курс')
button_delete = KeyboardButton('Удалить курс')

button_admin = ReplyKeyboardMarkup(resize_keyboard=True).add(button_load).add(button_delete)