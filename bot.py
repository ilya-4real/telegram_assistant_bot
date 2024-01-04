from aiogram import Dispatcher, Bot
from aiogram.enums import ParseMode

import logging
import sys
from config import API_KEY
import asyncio
from services.task_service import scheduler

from app.handlers import routers


async def main():
    bot = Bot(API_KEY, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    dp.include_routers(*routers)
    scheduler.start()
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
