from aiogram.dispatcher.filters.state import State, StatesGroup


class Add(StatesGroup):
    id_tg = State()
    surname = State()
    name = State()
    middlename = State()
    year_of_birth = State()
    rank = State()