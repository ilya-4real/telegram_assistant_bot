from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import text

import re

from database.users import UsersRepository
from ..states import UserState


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
    msg = text("your saved on server data is:",
               f'user id : {res[0].id}',
               f'username : {res[0].username}',
               f'email : {res[0].email} ',
               f'verified: {res[0].is_verified}',
               f'date of registration : {res[0].registered_at}',
               sep='\n'
               )
    await message.answer(msg)


@router.message(Command("addemail"))
async def user_email_handler(message: Message):
    found_email = re.search(r"( .*@\w+\.\w+)", message.text)
    if found_email is not None:
        ready_email = found_email.group().strip()
        await UsersRepository().set_email(message.from_user.id, ready_email)
        await message.answer("successfully added your email!")
    else:
        await message.answer("invalid email. try again")


@router.message(Command("weather"), UserState.all_set)
async def weather_handler(message: Message) -> None:
    weather = "none"
    await message.answer(weather)
