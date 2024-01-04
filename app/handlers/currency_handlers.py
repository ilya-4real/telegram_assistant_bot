from ..states import CurrencyForm
from aiogram import Router
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

from ..keyboards import build_keyboard
from .. import messages
from services import CurrencyService, ImageService
from exceptions import UserCurrencyNotSet


router = Router()


@router.message(Command("add_currency"))
async def get_currency_symbol_from_user(message: Message, state: FSMContext):
    await state.set_state(CurrencyForm.setting_currency)
    await message.answer("Okay, send me currency symbol accoring to ISO-4217")


@router.message(CurrencyForm.setting_currency)
async def set_user_currency(message: Message, state: FSMContext):
    symbol = CurrencyService().check_currency_symbol(message.text)
    await state.update_data(symbol=symbol)
    await state.set_state(CurrencyForm.make_sure)
    keyboard = build_keyboard('Yes', 'No')
    await message.answer(
        f"Your selected symbol is {symbol}. is it correct?",
        reply_markup=keyboard
        )


@router.message(CurrencyForm.make_sure)
async def make_sure_currency(message: Message, state: FSMContext):
    data = await state.get_data()
    if message.text == 'Yes':
        await CurrencyService().add_currency_to_user(
            data['symbol'], message.from_user.id)
        await message.answer(
            'The symbol has been added to your profile',
            reply_markup=ReplyKeyboardRemove()
            )
        await state.clear()
    else:
        await state.clear()
        await message.answer(
            "Okey, Try again later.",
            reply_markup=ReplyKeyboardRemove()
            )


@router.message(Command("currency"))
async def get_currency_rates(message: Message):
    try:
        rates = await CurrencyService().get_currency_rates(message.from_user.id)
        image_id = await ImageService.get_image_id('currency')
        msg = messages.get_cur_message(rates)
        await message.answer_photo(image_id, msg)
    except UserCurrencyNotSet as e:
        await message.answer(str(e))
