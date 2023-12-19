from ..states import CurrencyForm
from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from services.currency_service import CurrencyService

from .. import messages

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
    await message.answer(f"Your selected symbol is {symbol}. is it correct?")


@router.message(CurrencyForm.make_sure)
async def make_sure_currency(message: Message, state: FSMContext):
    data = await state.get_data()
    if message.text == 'yes':
        await CurrencyService().add_currency_to_user(data['symbol'], message.from_user.id)
    else:
        await state.set_state(CurrencyForm.setting_currency)
        await message.answer("Okey, send me currency symbol again.")


@router.message(Command('view_currencies'))
async def get_user_currency_symbols(message: Message):
    symbols = await CurrencyService().get_user_symbols(user_id=message.from_user.id)
    print(symbols)
    await message.answer("your symbols are")


@router.message(Command("currencies"))
async def get_currency_rates(message: Message):
    rates = await CurrencyService().get_currency_rates(message.from_user.id)
    print(rates)
    msg = messages.get_cur_message(rates)
    await message.answer(msg)
