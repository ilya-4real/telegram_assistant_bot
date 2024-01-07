from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.exceptions import InvalidCity
from app.messages import welcome_message, getme_message, weather_message, common_message
from app.services import CurrencyService, WeatherService, UsersService, ImageService

router = Router()
dropstate_router = Router()


@router.message(CommandStart())
async def start_handler(message: Message) -> None:
    try:
        await UsersService.add_user(
            user_id=message.from_user.id, username=message.from_user.username
        )
        await message.answer(welcome_message())
    except:
        await message.answer("How can I help you?")


@router.message(Command("getme"))
async def get_my_info(message: Message):
    user = UsersService
    currency = CurrencyService()
    user = await user.get_user(message.from_user.id)
    symbols = await currency.get_user_currency_symbols(message.from_user.id)
    answer = getme_message(user, symbols)
    await message.answer(answer)


@router.message(Command("weather"))
async def weather_handler(message: Message) -> None:
    user_id = message.from_user.id
    image_id = await ImageService.get_image_id("weather")
    try:
        weather = await WeatherService().get_weather(user_id)
        msg = weather_message(weather)
        await message.answer_photo(image_id, msg)
    except InvalidCity:
        await message.answer(
            "You haven't set your city or your city is incorrect. Set it using /set_city command"
        )


@dropstate_router.message(Command("dropstate"))
async def drop_state(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Okay, now you don't have a state")


@router.message()
async def send_common_msg(message: Message):
    await message.answer(common_message())
