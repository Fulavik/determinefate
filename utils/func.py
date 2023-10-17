import json
from .keyboards import *
from .database.base import *
from .parser import *

from .states.find import Add

from aiogram.types import CallbackQuery, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext

from bot import dispatcher as dp

LANGUAGES = {
    "ru": "Русский",
    "by": "Беларускі"
}

file = open("./utils/languages.json", encoding='utf-8')
PHRASES = json.load(file)

async def get_user_language(user_id: int):
    user = await Users.filter(uid=user_id).first()
    if not user:
        return "ru"
    return user.language

async def get_phrases(language: str):
    with open(f'/utils/languages/{language}.json', 'r', encoding='utf-8') as file:
        translations = json.load(file)
        
    return translations

def check_canceled(funcion):
    async def decorator_access(message, state):
        if message.text == "❌Отмена" or message.text == "❌Адмена":
            await state.finish()
            return await message.reply(f"⛔ {PHRASES[await get_user_language(message.from_id)]['error_cancel']}:", reply_markup=ReplyKeyboardRemove())
            
        return await funcion(message, state)
    return decorator_access

# async def get_phrase(language: str, phrase: str):
#     with open(f'/utils/languages/{language}.json', 'r', encoding='utf-8') as file:
#         translations = json.load(file)
        
#     return translations[phrase]