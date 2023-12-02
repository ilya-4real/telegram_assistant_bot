from aiogram import Dispatcher, Bot
from aiogram.enums import ParseMode
import logging
import sys
from config import API_KEY
import asyncio
from app.handlers import router


async def main():
    bot = Bot(API_KEY, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING, stream=sys.stdout)
    asyncio.run(main())
