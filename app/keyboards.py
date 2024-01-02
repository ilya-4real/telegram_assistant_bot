
from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


def build_keyboard(*button: str, adjust_level: int = 2) -> types.ReplyKeyboardMarkup:
    """Builds reply keybaords for message"""
    builder = ReplyKeyboardBuilder()
    for but in button:
        builder.add(types.KeyboardButton(text=but))
    builder.adjust(adjust_level)
    return builder.as_markup(resize_keyboard=True)


def inline_kb_builder(page: int) -> types.InlineKeyboardMarkup:
    """Build inline keyboard for task message"""
    builder = InlineKeyboardBuilder()
    if page >= 1:
        builder.add(
            types.InlineKeyboardButton(
                text='Previous', 
                callback_data=f'prev_{page - 1}')
                )
    builder.add(
        types.InlineKeyboardButton(
            text='Next', 
            callback_data=f'next_{page + 1}')
            )
    return builder.as_markup()
