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

PHRASES = {
    "ru": {
        "choosed_language": "Вы выбрали русский язык",
        "already_state": "Вы уже начали заполнение информации, отмените его, что-бы начать новое.",

        "input_name": "Введите имя: ",
        "input_surname": "Введите фамилию: ",
        "input_middlename": "Введите отчество: ",
        "input_year_of_birth": "Введите год рождения: ",
        "input_rank": "Введите звание: ",

        "check_inputed_info": "Проверьте ввёденную информацию",
        "name": "Имя",
        "surname": "Фамилия",
        "middlename": "Отчество",
        "year_of_birth": "Год рождения",
        "rank": "Звание"
    },

    "by": {
        "choosed_language": "Вы выбралі беларускую мову",
        "already_state": "Вы ўжо пачалі запаўненне інфармацыі, адменіце гэта, каб пачаць новае.",

        "input_name": "Увядзіце імя: ",
        "input_surname": "Увядзіце прозвішча: ",
        "input_middlename": "Увядзіце імя па бацьку: ",
        "input_year_of_birth": "Увядзіце год нараджэння: ",
        "input_rank": "Увядзіце званне: ",

        "check_inputed_info": "Праверце ўведзеную інфармацыю",
        "name": "Імя",
        "surname": "Прозвішча",
        "middlename": "Імя па бацьку",
        "year_of_birth": "Год нараджэння",
        "rank": "Званне" 
    }   
}

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
        if message.text == "❌Отмена":
            return await message.reply(f"⛔ Поиск информации отменён", reply_markup=ReplyKeyboardRemove())
            
        return await funcion(message, state)
    return decorator_access

# async def get_phrase(language: str, phrase: str):
#     with open(f'/utils/languages/{language}.json', 'r', encoding='utf-8') as file:
#         translations = json.load(file)
        
#     return translations[phrase]