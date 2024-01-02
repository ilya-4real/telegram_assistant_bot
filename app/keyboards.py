from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def build_keyboard(*button: str, adjust_level: int = 2) -> ReplyKeyboardMarkup:
    """Builds reply keybaords for message"""
    builder = ReplyKeyboardBuilder()
    for but in button:
        builder.add(KeyboardButton(text=but))
    builder.adjust(adjust_level)
    return builder.as_markup(resize_keyboard=True)


def inline_kb_builder(*button: str, callback_data: str):
    """Build inline keyboard for message"""
    builder = InlineKeyboardBuilder()
    for but in button:
        builder.add(InlineKeyboardButton(text=but, callback_data=callback_data))
    return builder.as_markup()
