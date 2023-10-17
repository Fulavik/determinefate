from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def get_language_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("🇷🇺 Русский", callback_data="language:ru"),
        InlineKeyboardButton("🇧🇾 Беларускі", callback_data="language:by"),
    )
    return keyboard

async def get_accept_keyboard(cancel):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("✅Да", callback_data="accept"),
        InlineKeyboardButton(f"❌{cancel}", callback_data="cancel"),
    )
    return keyboard

async def get_find_keyboard(after: bool = False, state: str = None):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("Отменить", callback_data="cancel"),
    )

    if after == True:
        keyboard.add(
            InlineKeyboardButton("Пропустить", callback_data=f"skip:{state}"),
        )

    return keyboard
