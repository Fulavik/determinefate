import random
from aiogram import types
from aiogram.dispatcher.filters import Command, Text

from utils.func import *

file = open('./utils/facts.json', encoding='utf-8')
FACTS = json.load(file)["facts"]

@dp.message_handler(Command("facts", ignore_case=True))
async def _facts(message: types.Message):
    random_fact = random.choice(FACTS)

    fact_text = random_fact["fact"]
    fact_description = random_fact["description"]
    
    await message.reply("<b>" + fact_text + "</b>\n\n" + fact_description)
