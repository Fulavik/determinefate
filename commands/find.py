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
    await state.update_data(uid=uid)

    await Add.name.set()
    await message.reply('Введите имя: ')


@dp.message_handler(state=Add.name)
async def add_surname(message: types.Message, state: FSMContext):
    await message.reply('Введите фамилию: ')
    await state.update_data(name=message.text)
    await Add.surname.set()


@dp.message_handler(state=Add.surname)
async def add_middlename(message: types.Message, state: FSMContext):
    keyboard = await get_find_keyboard(True, "middlename")
    await message.reply('Введите отчество: ')
    await state.update_data(surname=message.text)
    await Add.middlename.set()

@dp.message_handler(state=Add.middlename)
async def add_date(message: types.Message, state: FSMContext):
    await message.reply('Введите год рождения: ')
    await state.update_data(middlename=message.text)
    await Add.next()


@dp.message_handler(state=Add.year_of_birth)
async def add_rank(message: types.Message, state: FSMContext):
    await message.reply('Введите звание: ')
    await state.update_data(year_of_birth=int(message.text))
    await Add.next()


@dp.message_handler(state=Add.rank)
async def rank(message: types.Message, state: FSMContext):
    await state.update_data(rank=message.text)
    async with state.proxy() as data:
        form = CreatedForm(**data)

    await message.reply(f"""
<b>Проверьте ввёденную информацию:</b>
<b>Имя: </b> {form.name}
<b>Фамилия: </b> {form.surname}
<b>Отчество: </b> {form.middlename}
<b>Год рождения: </b> {form.year_of_birth}
<b>Звание: </b> {form.rank}
""")
    await Add.next()

@dp.message_handler(Text('Да', ignore_case=True))
async def yes_form(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        form = CreatedForm(**data)
    await state.finish()

    Queries.create(uid=message.from_id, name=form.name, surname=form.surname,
                middlename=form.middlename, year_of_birth=form.year_of_birth,
                rank=form.rank)

    parse = await get_partizans(form.surname, form.name, form.middlename, form.year_of_birth, form.rank)
    await message.reply(parse)