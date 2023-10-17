from aiogram import types
from aiogram.dispatcher.filters import Command, Text

from utils.func import *

@dp.message_handler(Command("facts", ignore_case=True))
async def _facts(message: types.Message):
    pass

    # await message.reply(PHRASES[language]["input_name"], reply_markup=keyboard)