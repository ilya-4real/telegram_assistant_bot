from aiogram import Dispatcher, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.enums import ParseMode
import logging
import sys
from config import API_KEY
import asyncio
from weather import get_weather

dp = Dispatcher()

@dp.message(CommandStart())
async def start_handler(message: Message) -> None:
    await message.answer(f'Hello, {message.from_user.first_name}')

@dp.message(Command("weather"))
async def weather_handler(message: Message) -> None:
    weather = await get_weather()
    answer = str(weather['main']['temp']-273.15)
    await message.answer(answer)


async def main():
    bot = Bot(API_KEY, parse_mode=ParseMode.HTML)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
