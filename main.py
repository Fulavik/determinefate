"""Запуск Бота"""

import aiogram

from bot import on_startup
from commands import dp

aiogram.executor.start_polling(dp, on_startup=on_startup, skip_updates=True)