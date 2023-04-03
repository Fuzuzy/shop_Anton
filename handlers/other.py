from create_bot import dp, bot
from aiogram import types, Dispatcher


# @dp.message_handler()
async def echo_test(message: types.Message):
    await message.answer(message.text)


def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(echo_test)
