from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states import CityForm


router = Router()


@router.message(Command("set_city"))
async def get_city(message: Message, state: FSMContext):
    await state.set_state(CityForm.setting_city)
    await message.answer("Alright, send the name of your city")


@router.message(CityForm.setting_city)
async def set_city(message: Message, state: FSMContext):
    city = message.text
