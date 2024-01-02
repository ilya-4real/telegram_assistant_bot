from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from services import email_service, user_service
from services.exceptions import InvalidEmail
from ..states import EmailForm

router = Router()


@router.message(Command("verify_email"))
async def start_email_setting(message: Message, state: FSMContext):
    await state.set_state(EmailForm.setting_email)
    await message.answer("Okey. Send me your email address")


@router.message(EmailForm.setting_email)
async def set_email(message: Message, state: FSMContext):
    try:
        code = await email_service.send_email(message.from_user.username, message.text)
        await state.update_data(verification_code=str(code), user_email=message.text)
        await state.set_state(EmailForm.code_sent)
        await message.answer("Good! I've sent you an email with a code."
                             "Please enter the code in the next message")
    except InvalidEmail as e:
        await message.answer(str(e))


@router.message(EmailForm.code_sent)
async def check_code(message: Message, state: FSMContext):

    user_sent_code = message.text
    state_data = await state.get_data()
    sent_code = state_data['verification_code']
    user_email = state_data['user_email']

    if not user_sent_code.isdigit():
        await message.answer("code consists only of numbers")
    else:
        if sent_code != user_sent_code:
            await message.answer("Bad numbers! Try again.")
        else:
            await user_service.UsersService().set_email(message.from_user.id, user_email)
            await state.clear()
            await message.answer(
                "Great! Your email is verified. "
                "Now you can use every feature that I provide)")
