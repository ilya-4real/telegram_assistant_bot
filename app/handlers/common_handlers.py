from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from .. import messages
from APIs.api_gate import FacadeApiGateway
from services.user_service import UsersService

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message) -> None:
    user_id = await UsersService().add_user(
        user_id=message.from_user.id,
        username=message.from_user.username
        )
    await message.answer(
        f'Hello, {message.from_user.first_name}, your id is {user_id}'
        )
        

@router.message(Command("getme"))
async def get_my_info(message: Message):
    res = await UsersService().get_user(message.from_user.id)
    answer = messages.getme_message(res)
    await message.answer(answer)


@router.message(Command("weather"))
async def weather_handler(message: Message) -> None:
    city = await UsersService().get_city(message.from_user.id)
    weather = await FacadeApiGateway(city).get_weather()
    msg = messages.weather_message(weather)
    await message.answer_photo("AgACAgIAAxkBAAIC8WWAjfQJlYSMn0EiwforOJUAAV_xCQAC688xG2VLCEgsDuhwgiBt0gEAAwIAA20AAzME", caption=msg)


@router.message(Command("dropstate"))
async def drop_state(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Okay, now you don't have a state")


@router.message()
async def common_handler(message: Message):
    answer_message = messages.common_message()
    await message.answer(answer_message)

