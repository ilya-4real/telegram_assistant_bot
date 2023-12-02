from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from database.users import UsersRepository
from APIs.weather import get_weather
from aiogram.utils.markdown import text
import re


router = Router()


@router.message(CommandStart())
async def start_handler(message: Message) -> None:
    user_id =  await UsersRepository().add_one(id=message.from_user.id, username=message.from_user.username)
    await message.answer(f'Hello, {message.from_user.first_name}, your id = {user_id}')


@router.message(Command("getme"))
async def get_my_info(message: Message):
    res = await UsersRepository().get_one(id=message.from_user.id)
    print(res[0].id)
    print(res, res==None)
    msg = text("your saved on server data is:", 
               f'user id : {res[0].id}',
               f'username : {res[0].username}',
               f'email : {res[0].email} ',
               f'date of starting : {res[0].registered_at}',
               sep='\n'
               )
    msg_content = re.search(r"( .*@\w+\.\w+)", message.text)
    print(msg_content.group())
    await message.answer(msg, parse_mode="MARKDOWN")


@router.message(Command("addemail"))
async def user_email_handler(message: Message):
    found_email = re.search(r"( .*@\w+\.\w+)", message.text)
    if found_email is not None: 
        ready_email = found_email.group().strip()
        await UsersRepository().add_user_email(message.from_user.id, ready_email)
        await message.answer("successfully added your email!")
    else:
        await message.answer("invalid email. try again")


@router.message(Command("weather"))
async def weather_handler(message: Message) -> None:
    weather = await get_weather()
    answer = str(round(weather['main']['temp']-273.15))
    await message.answer(answer)
