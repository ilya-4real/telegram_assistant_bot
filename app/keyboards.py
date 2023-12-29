from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def build_keyboard(*button: str, adjust_level: int = 2) -> ReplyKeyboardMarkup:
    """Builds reply keybaords for message"""
    builder = ReplyKeyboardBuilder()
    for but in button:
        builder.add(KeyboardButton(text=but))
    builder.adjust(adjust_level)
    return builder.as_markup(resize_keyboard=True)
