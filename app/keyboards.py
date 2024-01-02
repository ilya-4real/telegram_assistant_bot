
from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

from database.models import Task


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


def tasks_kb(tasks: list[Task], start_page):
    builder = InlineKeyboardBuilder()
    buttons = []
    for task in tasks:
        builder.row(types.InlineKeyboardButton(text=task.title, callback_data=f'taskdetail_{task.id}'))
    if start_page >= 1:
        buttons.append(
            types.InlineKeyboardButton(
                text='Previous', 
                callback_data=f'prev_{start_page - 1}')
                )
    buttons.append(
        types.InlineKeyboardButton(
            text='Next', 
            callback_data=f'next_{start_page + 1}'))
    builder.row(*buttons)
    return builder.as_markup()


def task_detail_kb(task: Task):
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text='Title',
            callback_data=TaskCallbackFactory(action='title', task_id=task.id).pack()
        ),
        types.InlineKeyboardButton(
            text='Description',
            callback_data=TaskCallbackFactory(action='description', task_id=task.id).pack()
        ),
        types.InlineKeyboardButton(
            text='Date',
            callback_data=TaskCallbackFactory(action='date', task_id=task.id).pack()
        ),  
        types.InlineKeyboardButton(
            text='time',
            callback_data=TaskCallbackFactory(action='time', task_id=task.id).pack()
        ), 
    )
    builder.row(
        types.InlineKeyboardButton(
            text='Delete',
            callback_data=TaskCallbackFactory(action='delete', task_id=task.id).pack()
        ),
        types.InlineKeyboardButton(
            text='task_nothing',
            callback_data=TaskCallbackFactory(action='nothing', task_id=task.id).pack()
        )
    )
    return builder.as_markup()

def ask_to_delete_kb(task_id: int):
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text='Yes',
            callback_data=TaskCallbackFactory(action='reallydelete', task_id=task_id).pack()
        ),
        types.InlineKeyboardButton(
            text='No',
            callback_data=TaskCallbackFactory(action='notdelete', task_id=task_id).pack()
        )
    )
    return builder.as_markup()

class TaskCallbackFactory(CallbackData, prefix='task'):
    action: str
    task_id: int