from aiogram import Dispatcher, Bot
from aiogram.enums import ParseMode

import logging
import sys
from config import API_KEY
import asyncio

from app.handlers.common_handlers import router as main_router
from app.handlers.task_handlers import router as task_router
from app.handlers.email_verify_handler import router as email_router
from app.handlers.city_handlers import router as city_router


async def main():
    bot = Bot(API_KEY, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    dp.include_routers(main_router, task_router, email_router, city_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
