from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from .. import messages
from services import api_services, user_service

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message) -> None:
    user_id = await user_service.UsersService().add_user(
        user_id=message.from_user.id,
        username=message.from_user.username
        )
    await message.answer(
        f'Hello, {message.from_user.first_name}, your id is {user_id}'
        )


@router.message(Command("getme"))
async def get_my_info(message: Message):
    user = user_service.UsersService()
    currency = api_services.CurrencyService()
    user = await user.get_user(message.from_user.id)
    symbols = await currency.get_user_currency_symbols(message.from_user.id)
    answer = messages.getme_message(user, symbols)
    await message.answer(answer)


@router.message(Command('show_info'))
async def get_todays_info(message: Message):
    user_id = message.from_user.id 
    data = await api_services.InfoService().get_info(user_id)
    msg = messages.todays_info_message(data)
    await message.answer(msg)


@router.message(Command("weather"))
async def weather_handler(message: Message) -> None:
    user_id = message.from_user.id
    weather = await api_services.WeatherService().get_weather(user_id)
    msg = messages.weather_message(weather)
    await message.answer(msg)


@router.message(Command("dropstate"))
async def drop_state(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Okay, now you don't have a state")
