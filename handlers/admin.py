from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import dp, bot
from aiogram.dispatcher.filters import Text
from keyboards import admin_kb
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from data_base import sqlite_db


class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()
    url = State()


async def admin_login(message: types.Message):
    ID = message.from_user.id
    if ID == 831404222:
        await bot.send_message(message.from_user.id, "Выполнен вход как администратор",
                               reply_markup=admin_kb.button_admin)
        await message.delete()
    else:
        await bot.send_message(message.from_user.id, 'В доступе отказано')


# Начало диалога загрузки нового пункта меню
# @dp.message_handler(commands='Загрузить', state=None)
async def cm_start(message: types.Message):
    ID = message.from_user.id
    if ID == 831404222:
        await FSMAdmin.photo.set()
        await message.reply('Загрузи фото')



# Выход из состояния
# @dp.message_handler(state='*',commands='отмена')
# @dp.message_handler(Text(equals='отмена',ignore_case=True),state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('OK')


# Ловим первый ответ и пишем в словарь
# @dp.message_handler(content_types=['photo'], state=FSMAdmin.photo)
async def load_photo(message: types.Message, state: FSMContext):
    ID = message.from_user.id
    if ID == 831404222:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        await FSMAdmin.next()
        await message.reply("Теперь введи название")


# Ловим второй ответ
# @dp.message_handler(state=FSMAdmin.name)
async def load_name(message: types.Message, state: FSMContext):
    ID = message.from_user.id
    if ID == 831404222:
        async with state.proxy() as data:
            data['name'] = message.text
        await FSMAdmin.next()
        await message.reply("Введи описание")


# Ловим третий ответ
# @dp.message_handler(state=FSMAdmin.description)
async def load_description(message: types.Message, state: FSMContext):
    ID = message.from_user.id
    if ID == 831404222:
        async with state.proxy() as data:
            data['description'] = message.text
        await FSMAdmin.next()
        await message.reply("Теперь укажи цену")


# Ловим последний ответ и используем полученные данные
# @dp.message_handler(state=FSMAdmin.price)
async def load_price(message: types.Message, state: FSMContext):
    ID = message.from_user.id
    if ID == 831404222:
        async with state.proxy() as data:
            data['price'] = float(message.text)
        await FSMAdmin.next()
        await message.reply("Теперь укажи ссылку")


async def load_url(message: types.Message, state: FSMContext):
    ID = message.from_user.id
    if ID == 831404222:
        async with state.proxy() as data:
            data['url'] = message.text
        await sqlite_db.sql_add_command(state)
        await state.finish()
        await message.reply("Готово")


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('del '))
async def del_callback_run(callback_query: types.CallbackQuery):
    await sqlite_db.sql_delete_command(callback_query.data.replace('del ', ''))
    await callback_query.answer(text=f'{callback_query.data.replace("del ", "")} - удалено.', show_alert=True)


@dp.message_handler(Text(equals="Удалить курс"))
async def delete_item(message: types.Message):
    ID = message.from_user.id
    if ID == 831404222:
        read = await sqlite_db.sql_read2()
        for ret in read:
            await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nОписание: {ret[2]}\nЦена {ret[-1]}')
            await bot.send_message(message.from_user.id, text='^^^^^^^^^^^^^^^^^^^^',
                                   reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(f"Удалить {ret[1]}",
                                                                                                callback_data=f"del {ret[1]}")))


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(admin_login, Text(equals="Админ"))
    dp.register_message_handler(cm_start, Text(equals="Загрузить курс"), state=None)
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(load_price, state=FSMAdmin.price)
    dp.register_message_handler(load_url, state=FSMAdmin.url)
    dp.register_message_handler(cancel_handler, state='*', commands=['отмена'])
