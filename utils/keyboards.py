from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def get_language_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("🇷🇺 Русский", callback_data="language:ru"),
        InlineKeyboardButton("🇧🇾 Беларускі", callback_data="language:by"),
    )
    return keyboard