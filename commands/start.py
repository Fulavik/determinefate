from aiogram import types
from aiogram.dispatcher.filters import Command
from utils.func import *


@dp.message_handler(Command('start', ignore_case=True))
async def send_welcome(message: types.Message):    
    args = message.get_args()
    if args.startswith("id_"):
        id = message.get_args().replace("id_", "")
        partizan = await get_partizan_by_id(id)
        if partizan is None:
            return await message.answer("Произошла ошибка.")

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
"""
        return await message.reply(text)
    elif args.startswith("search_"):
        id = message.get_args().replace("search_", "")
        query = await Queries.filter(id=id).first()

        if not query:
            return await message.answer("Произошла ошибка.")

        parse = await get_partizans(query.name, query.surname, query.middlename, query.year_of_birth, query.rank)

        if not parse:
            return await message.reply("Ничего не найдено!")

        buttons = InlineKeyboardMarkup(row_width=2)
        number = 0
        text = "<b>На клавиатуре с кнопками выберите нужного человека по номеру:\n</b>"

        for i in parse:
            number = number + 1
            text += f"{number}. {parse[i]['full_name']} [ID: {i}] | {parse[i]['date_of_birth']} | {parse[i]['date_of_die']}\n"
            buttons.add(InlineKeyboardButton(text=f"{parse[i]['full_name']} [ID: {i}]", callback_data=f"find:{i}"))

        text += f"\nСсылка на результат: https://t.me/fmtestpython_bot?start=search_{query.id}"

        return await message.reply(text, reply_markup=buttons)

    keyboard = await get_language_keyboard()
    await message.reply("<b>⚙️ Выберите язык/Абярыце мову</b>", reply_markup=keyboard)

@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith("language"))
async def choose_language(callback_query: CallbackQuery, state: FSMContext):
    lang = callback_query.data.split(":")[1]

    user = await Users.filter(uid=callback_query.from_user.id).first()

    if not user == None:
        user.language = lang
        await user.save()
        return await callback_query.message.reply("Вы выбрали язык: " + LANGUAGES[lang])

    await Users.create(uid=callback_query.from_user.id, language = lang)

    await callback_query.message.reply("Вы выбрали язык: " + LANGUAGES[lang])
