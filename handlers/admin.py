from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import dp, bot
from aiogram.dispatcher.filters import Text
from keyboards import admin_kb
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()


async def admin_login(message: types.Message):
    ID = message.from_user.id
    if ID == 831404222:
        await bot.send_message(message.from_user.id, "Выполнен вход как администратор", reply_markup=admin_kb.button_admin)
        await message.delete()
    else:
        await bot.send_message(message.from_user.id, 'В доступе отказано')

def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(admin_login, Text(equals="Админ"))