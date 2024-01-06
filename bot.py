from aiogram import Dispatcher, Bot
from aiogram.enums import ParseMode

from app.config import API_KEY
from app.services.task_service import scheduler

from app.handlers import routers


bot = Bot(API_KEY, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot=bot)


async def main():
    
    dp.include_routers(*routers)
    scheduler.start()
