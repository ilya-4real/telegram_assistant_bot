from .. states import EmailForm
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from services.email_verification import check_email, send_email


router = Router()


@router.message(Command("verifyemail"))
async def start_email_setting(message: Message, state: FSMContext):
    await state.set_state(EmailForm.setting_email)
    await message.answer("Good. Send your email address")


@router.message(EmailForm.setting_email)
async def set_email(message: Message, state: FSMContext):
    email = check_email(message.text)
    if email is not None:
        await message.answer("Good! I sent you an email with a code."
                             "Please enter the code in the next message")
        await send_email(message.from_user.username, email)
        await state.set_state(EmailForm.code_sent)
    else:
        await message.answer("Something wrong with your email(. Send it again")
        