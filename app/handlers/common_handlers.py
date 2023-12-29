from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from .. import messages
from APIs.api_gate import FacadeApiGateway
from services import user_service, currency_service

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
    currency = currency_service.CurrencyService()
    user = await user.get_user(message.from_user.id)
    symbols = await currency.get_user_currency_symbols(message.from_user.id)
    answer = messages.getme_message(user, symbols)
    await message.answer(answer)


@router.message(Command("weather"))
async def weather_handler(message: Message) -> None:
    city = await user_service.UsersService().get_city(message.from_user.id)
    print(city)
    weather = await FacadeApiGateway(city).get_weather()
    msg = messages.weather_message(weather)
    await message.answer(msg)


@router.message(Command("dropstate"))
async def drop_state(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Okay, now you don't have a state")


# @router.message()
# async def common_handler(message: Message):
#     answer_message = messages.common_message()
#     await message.answer(answer_message)
