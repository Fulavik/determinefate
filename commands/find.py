from aiogram import types
from aiogram.dispatcher.filters import Command, Text

from pydantic import BaseModel
from utils.func import *


class CreatedForm(BaseModel):
    uid: int
    surname: str
    name: str
    middlename: str
    year_of_birth: int
    rank: str


@dp.message_handler(Command("find", ignore_case=True))
async def find(message: types.Message, state: FSMContext):
    uid = message.from_id
    language = await get_user_language(uid)
    is_state = dp.current_state(user=message.from_user).get_state()

    if is_state:
        return await message.reply(f"Вы уже начали заполнение информации, отмените его, что-бы начать новое")

    await state.update_data(uid=uid)

    await Add.name.set()
    await message.reply(PHRASES[language]["input_name"])


@dp.message_handler(state=Add.name)
async def add_surname(message: types.Message, state: FSMContext):
    await message.reply(PHRASES[await get_user_language(message.from_id)]["input_surname"])
    await state.update_data(name=message.text)
    await Add.surname.set()


@dp.message_handler(state=Add.surname)
async def add_middlename(message: types.Message, state: FSMContext):
    await message.reply(PHRASES[await get_user_language(message.from_id)]["input_middlename"])
    await state.update_data(surname=message.text)
    await Add.middlename.set()

@dp.message_handler(state=Add.middlename)
async def add_date(message: types.Message, state: FSMContext):
    await message.reply(PHRASES[await get_user_language(message.from_id)]["input_year_of_birth"])
    await state.update_data(middlename=message.text)
    await Add.next()


@dp.message_handler(state=Add.year_of_birth)
async def add_rank(message: types.Message, state: FSMContext):
    await message.reply(PHRASES[await get_user_language(message.from_id)]["input_rank"])
    await state.update_data(year_of_birth=int(message.text))
    await Add.next()


@dp.message_handler(state=Add.rank)
async def rank(message: types.Message, state: FSMContext):
    language = await get_user_language(message.from_id)
    await state.update_data(rank=message.text)
    async with state.proxy() as data:
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

