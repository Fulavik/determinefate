import aiogram, logging, os

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from utils.database.initializate import setup_db
from dotenv import load_dotenv


load_dotenv()


bot = Bot(token=os.getenv("TOKEN"), parse_mode="HTML")
dispatcher = aiogram.Dispatcher(bot, storage=MemoryStorage())

logging.basicConfig(level=logging.INFO)

async def on_startup(dispatcher):
    await setup_db()