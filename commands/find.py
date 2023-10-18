from aiogram import types
from aiogram.dispatcher.filters import Command, Text

from pydantic import BaseModel
from utils.func import *

def kb2(language):
    return [[types.KeyboardButton(text=f'➡️{PHRASES[language]["skip"]}')],[types.KeyboardButton(text=f'❌{PHRASES[language]["cancel"]}')]]

def kb(language):  
    return [[types.KeyboardButton(text=f'❌{PHRASES[language]["cancel"]}')]]

def kb3(language):  
    return [[types.KeyboardButton(text=f'➡️Да')], [types.KeyboardButton(text=f'❌{PHRASES[language]["cancel"]}')]]

class CreatedForm(BaseModel):
    uid: int
    surname: str
    name: str
    middlename: str
    year_of_birth: int
    rank: str
    accepter: str

@dp.message_handler(Command("find", ignore_case=True))
@check_canceled
async def find(message: types.Message, state: FSMContext):
    uid = message.from_id
    language = await get_user_language(uid)
    is_state = await dp.current_state(user=message.from_user).get_state()

    if is_state:
        return await message.reply(f"🚥 {PHRASES[language]['already_state']}")

    await state.update_data(uid=uid)
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb(await get_user_language(message.from_id)), resize_keyboard=True)

    await Add.name.set()
    await message.reply(f'🧍 {PHRASES[language]["input_name"]}:', reply_markup=keyboard)


@dp.message_handler(state=Add.name)
@check_canceled
async def add_surname(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb(await get_user_language(message.from_id)), resize_keyboard=True)
    await message.reply(f'🧍 {PHRASES[await get_user_language(message.from_id)]["input_surname"]}:', reply_markup=keyboard)
    await state.update_data(name=message.text)
    await Add.surname.set()

@dp.message_handler(state=Add.surname)
@check_canceled
async def add_middlename(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb2(await get_user_language(message.from_id)), resize_keyboard=True)
    await message.reply(f'🧑‍🦳 {PHRASES[await get_user_language(message.from_id)]["input_middlename"]}:', reply_markup=keyboard)
    await state.update_data(surname=message.text)
    await Add.middlename.set()

@dp.message_handler(state=Add.middlename)
@check_canceled
async def add_date(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb2(await get_user_language(message.from_id)), resize_keyboard=True)
    await message.reply(f'🎂 {PHRASES[await get_user_language(message.from_id)]["input_year_of_birth"]}:', reply_markup=keyboard)
    await state.update_data(middlename=message.text)
    await Add.year_of_birth.set()
    

@dp.message_handler(state=Add.year_of_birth)
@check_canceled
async def add_rank(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb2(await get_user_language(message.from_id)), resize_keyboard=True)
    
    if message.text == "➡️Пропустить" or message.text == "➡️Прапусціць":
        await message.reply(f'🎖️ {PHRASES[await get_user_language(message.from_id)]["input_rank"]}:', reply_markup=keyboard)
        await state.update_data(year_of_birth=0)
        return await Add.rank.set()

    if not message.text.isdigit():
        await message.reply(f'⛔ {PHRASES[await get_user_language(message.from_id)]["error_year"]}')
        return await Add.year_of_birth.set()
    
    await message.reply(f'🎖️ {PHRASES[await get_user_language(message.from_id)]["input_rank"]}:', reply_markup=keyboard)

    await state.update_data(year_of_birth=int(message.text))
    await Add.rank.set()

@dp.message_handler(state=Add.rank)
async def rank(message: types.Message, state: FSMContext):
    # keyboard = types.ReplyKeyboardMarkup(keyboard=kb2(await get_user_language(message.from_id)), resize_keyboard=True)

    language = await get_user_language(message.from_id)
    await state.update_data(rank=message.text, accepter="False")
    async with state.proxy() as data:
        
        for key, value in data.items():
            if value == '➡️Пропустить' or value == "➡️Прапусціць":
                data[key] = ""
    
        form = CreatedForm(**data)

    keyboard = types.ReplyKeyboardMarkup(keyboard=kb3(await get_user_language(message.from_id)), resize_keyboard=True)

    await message.reply(f"""
<b>{PHRASES[language]["check_inputed_info"]}:</b>
<b>{PHRASES[language]["name"]}: </b> {form.name}
<b>{PHRASES[language]["surname"]}: </b> {form.surname}
<b>{PHRASES[language]["middlename"]}: </b> {form.middlename}
<b>{PHRASES[language]["year_of_birth"]}: </b> {form.year_of_birth}
<b>{PHRASES[language]["rank"]}: </b> {form.rank}
""", reply_markup=keyboard)
    
    await Add.accepter.set()

@dp.message_handler(state=Add.accepter)
async def rank(message: types.Message, state: FSMContext):
    accepter = message.text 
    

    if accepter == f"❌{PHRASES[await get_user_language(message.from_id)]['cancel']}":
        return
    
    if accepter == "➡️Да":
        async with state.proxy() as data:
            form = CreatedForm(**data)
        await state.finish()

        query = await Queries.create(uid=message.from_id, name=form.name, surname=form.surname,
                    middlename=form.middlename, year_of_birth=form.year_of_birth,
                    rank=form.rank)

        parse = await get_partizans(form.surname, form.name, form.middlename, form.year_of_birth, form.rank)
        if not parse:
            return await message.reply("Ничего не найдено!")

        buttons = InlineKeyboardMarkup(row_width=2)
        number = 0
        text = "<b>На клавиатуре с кнопками выберите нужного человека по номеру:\n</b>"

        for i in parse:
            number = number + 1
            text += f"{number}. {parse[i]['full_name']} [ID: {i}] | {parse[i]['date_of_birth']} | {parse[i]['date_of_die']}\n"
            buttons.add(InlineKeyboardButton(text=f"{number}. {parse[i]['full_name']} [ID: {i}]", callback_data=f"find:{i}"))

        text += f"\nСсылка на результат: https://t.me/determinefateBot?start=search_{query.id}"

        await message.reply(text, reply_markup=buttons)

@dp.callback_query_handler(lambda c: c.data.startswith('find:'))
async def process_callback_button(callback_query: types.CallbackQuery):
    id = callback_query.data.split(':')[1]
    
    partizan = await get_partizan_by_id(id)
    if partizan is None:
        return await callback_query.answer("Произошла ошибка.")

    text = f"""
<b>Информация из донесения о безвозвратных потерях:</b>

ID: {id}

Фамилия: {partizan["surname"]}
Имя: {partizan["name"]}
Отчество: {partizan["middlename"]}
Дата рождения: {partizan["date_of_bitrh"]}
Место рождения: {partizan["place_of_birth"]}
Дата и место призыва: {partizan["call_place"]}
Последнее место службы: {partizan["last_call_place"]}
Воинское звание: {partizan["rank"]}
Причина выбытия: {partizan["reason_of_leave"]}
Дата выбытия: {partizan["date_of_leave"]}
Место выбытия: {partizan["place_of_leave"]}
Название источника донесения: {partizan["issue"]}

Ссылка на результат: https://t.me/determinefateBot?start=id_{id}
Информация была взята с сайта https://obd-memorial.ru/
"""

    await callback_query.message.reply(text)