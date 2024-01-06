from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from app.states import ImageForm
from app.services import UsersService, ImageService


router = Router()


@router.message(Command("setimage"))
async def start_setting_image(message: Message, state: FSMContext):
    if UsersService.check_is_admin(message.from_user.id):
        await state.set_state(ImageForm.choosing_category)
        await message.answer(
            "Alright, send me which category you wanna set (weather|currency|info) (case insensetive btw)"
        )


@router.message(ImageForm.choosing_category)
async def set_category(message: Message, state: FSMContext):
    category = message.text.lower()
    if category in ["weather", "currency", "info"]:
        await state.update_data(title=category)
        await state.set_state(ImageForm.setting_image)
        await message.answer("Good. Send an image please")
    else:
        await message.answer("Bad category. Send it again")


@router.message(ImageForm.setting_image)
async def set_image(message: Message, state: FSMContext):
    if not message.photo:
        await message.answer("There is no image. send it without jokes")
    else:
        state_data = await state.get_data()
        title = state_data['title']
        photo_id = message.photo[-1].file_id
        await ImageService.set_image(photo_id, title)
        await state.clear()
