from aiogram import types, Dispatcher
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from create_bot import dp, bot
from keyboards import kb_client
from aiogram.dispatcher.filters import Text
from data_base import sqlite_db

# Обработка старт и хелп
async def command_start(message: types.message):
    await bot.send_message(message.from_user.id,"Здесь будет описание\n"
                                                "Тут тоже\n"
                                                "Тут тоже\n"
                                                "Тут тоже\n",reply_markup=kb_client)


# @dp.message_handler(Text(equals="Test"))
async def support(message: types.Message):
    await message.answer("Связь с тех. поддержкой:\n"
                         "@Fuzuz")

@dp.message_handler(Text(equals="Список курсов"))
async def curse_menu_command(message: types.Message):
    await sqlite_db.sql_read(message)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(support, Text(equals="Техподдержка"))
    dp.register_message_handler(curse_menu_command, Text(equals="Список курсов"))
