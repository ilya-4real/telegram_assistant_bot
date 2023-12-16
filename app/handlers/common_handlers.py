from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import text

import re

from database.users import UsersRepository
from ..states import UserState
from ..messages import common_message, getme_message

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext) -> None:
    user_id = await UsersRepository().add_one(
        id=message.from_user.id,
        username=message.from_user.username
        )
    if user_id == 'already exists':
        await message.answer(f'your id {user_id}')
    else:
        await state.set_state(UserState.not_set)
        await message.answer(
            f'Hello, {message.from_user.first_name}, your id is {user_id}'
            )
        

@router.message(Command("getme"))
async def get_my_info(message: Message):
    res = await UsersRepository().get_one(id=message.from_user.id)
    answer = getme_message(res[0])
    await message.answer(answer)


@router.message(Command("weather"), UserState.all_set)
async def weather_handler(message: Message) -> None:
    weather = "none"
    await message.answer(weather)


@router.message(Command("dropstate"))
async def drop_state(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Okay, now you don't have a state")


# @router.message()
# async def common_handler(message: Message):
#     answer_message = common_message()
#     await message.answer(answer_message) 

