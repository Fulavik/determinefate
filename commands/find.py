from aiogram import types
from aiogram.dispatcher.filters import Command, Text

from pydantic import BaseModel
from utils.func import *

kb2 = [
        [types.KeyboardButton(text="➡️Пропустить")],
        [types.KeyboardButton(text="❌Отмена")],
    ]

kb = [[types.KeyboardButton(text="❌Отмена")]]

class CreatedForm(BaseModel):
    uid: int
    surname: str
    name: str
    middlename: str
    year_of_birth: int
    rank: str

@dp.message_handler(Command("find", ignore_case=True))
@check_canceled
async def find(message: types.Message, state: FSMContext):
    uid = message.from_id
    language = await get_user_language(uid)
    is_state = await dp.current_state(user=message.from_user).get_state()

    if is_state:
        return await message.reply(f"Вы уже начали заполнение информации, отмените его, что-бы начать новое")

    await state.update_data(uid=uid)
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    await Add.name.set()
    await message.reply(PHRASES[language]["input_name"], reply_markup=keyboard)


@dp.message_handler(state=Add.name)
@check_canceled
async def add_surname(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.reply(PHRASES[await get_user_language(message.from_id)]["input_surname"], reply_markup=keyboard)
    await state.update_data(name=message.text)
    await Add.surname.set()

@dp.message_handler(state=Add.surname)
@check_canceled
async def add_middlename(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb2, resize_keyboard=True)
    await message.reply(PHRASES[await get_user_language(message.from_id)]["input_middlename"], reply_markup=keyboard)
    await state.update_data(surname=message.text)
    await Add.middlename.set()

@dp.message_handler(state=Add.middlename)
@check_canceled
async def add_date(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb2, resize_keyboard=True)
    await message.reply(PHRASES[await get_user_language(message.from_id)]["input_year_of_birth"], reply_markup=keyboard)
    await state.update_data(middlename=message.text)
    await Add.next()

@dp.message_handler(state=Add.year_of_birth)
@check_canceled
async def add_rank(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb2, resize_keyboard=True)
    await message.reply(PHRASES[await get_user_language(message.from_id)]["input_rank"], reply_markup=keyboard)

    if message.text == "➡️Пропустить":
        await state.update_data(year_of_birth="➡️Пропустить")
        return await Add.next()

    if not message.text.isdigit():
       #Рома фиксани
       await state.set_state(Add.year_of_birth)
       return await message.reply(PHRASES[await get_user_language(message.from_id)]["error_year"])

    await state.update_data(year_of_birth=int(message.text))
    await Add.next()

@dp.message_handler(state=Add.rank)
async def rank(message: types.Message, state: FSMContext):
    # keyboard = types.ReplyKeyboardMarkup(keyboard=kb2, resize_keyboard=True)
    language = await get_user_language(message.from_id)
    await state.update_data(rank=message.text)
    async with state.proxy() as data:
        
        for key, value in data.items():
            if value == '➡️Пропустить':
                data[key] = ""
    
        form = CreatedForm(**data)

    

    await message.reply(f"""
<b>{PHRASES[language]["check_inputed_info"]}:</b>
<b>{PHRASES[language]["name"]}: </b> {form.name}
<b>{PHRASES[language]["surname"]}: </b> {form.surname}
<b>{PHRASES[language]["middlename"]}: </b> {form.middlename}
<b>{PHRASES[language]["year_of_birth"]}: </b> {form.year_of_birth}
<b>{PHRASES[language]["rank"]}: </b> {form.rank}
""")
    await Add.next()

@dp.message_handler(Text('Да', ignore_case=True))
async def yes_form(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        form = CreatedForm(**data)
    await state.finish()

    await Queries.create(uid=message.from_id, name=form.name, surname=form.surname,
                middlename=form.middlename, year_of_birth=form.year_of_birth,
                rank=form.rank)

    parse = await get_partizans(form.surname, form.name, form.middlename, form.year_of_birth, form.rank)
    await message.reply(parse)