from aiogram import types
from aiogram.dispatcher.filters import Command
from utils.func import *


@dp.message_handler(Command('start', ignore_case=True))
async def send_welcome(message: types.Message):    
    user = await Users.filter(uid=message.from_id).first()

    # if not user:
    keyboard = await get_language_keyboard()
    await message.reply("<b>⚙️ Выберите язык/Абярыце мову</b>", reply_markup=keyboard)
    # else:
    #     await message.answer("texttexttextr")

@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith("language"))
async def choose_language(callback_query: CallbackQuery, state: FSMContext):
    lang = callback_query.data.split(":")[1]

    await Users.create(uid=callback_query.from_user.id, language = lang)

    await callback_query.message.reply("Вы выбрали язык: " + LANGUAGES[lang])

    # part = await get_partizan_by_id(1002734)
    # await callback_query.message.reply(part)