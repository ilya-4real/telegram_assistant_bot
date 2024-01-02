from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from ..states import TaskForm
from services import datetime_service, task_service, user_service
from .. import messages
from ..keyboards import build_keyboard, ReplyKeyboardRemove, inline_kb_builder

router = Router()


@router.message(Command("addtask"))
async def start_task_form(message: Message, state: FSMContext):
    user_verified = await user_service.UsersService().check_email(message.from_user.id)
    if user_verified:
        await state.set_state(TaskForm.setting_title)
        await message.answer("The first step is the title of your task")
    else:
        await message.answer("You need to set email to your profile")


@router.message(TaskForm.setting_title)
async def set_task_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(TaskForm.setting_body)
    await message.answer("Good! next step is the task body")


@router.message(TaskForm.setting_body)
async def set_task_body(message:Message, state: FSMContext):
    await state.update_data(body=message.text)
    await state.set_state(TaskForm.setting_exp_date)
    await message.answer(
        "Great, almost done! Enter the task expiration date"
        " in format like dd-mm-yy"
        )


@router.message(TaskForm.setting_exp_date)
async def set_task_date(message: Message, state: FSMContext):
    try:
        date = datetime_service.check_date(message.text)
        await state.update_data(exp_date=date)
        await state.set_state(TaskForm.setting_exp_time)
        await message.answer(
            """Date successfully set.
              Send me exact time of expiration in format like hh-mm"""
            )
    except ValueError as e:
        await message.answer(str(e))
    

@router.message(TaskForm.setting_exp_time)
async def set_task_time(message: Message, state: FSMContext):
    try:
        time = datetime_service.check_time(message.text)
        await state.update_data(exp_time=time)
        await state.set_state(TaskForm.make_sure)
        data = await state.get_data()
        keyboard = build_keyboard('Yes', 'No')
        await message.answer(
            messages.check_task_message(**data),
            reply_markup=keyboard
            )
    except ValueError as e:
         await message.answer(str(e))


@router.message(TaskForm.make_sure)
async def add_task(message: Message, state: FSMContext):
    if message.text == 'Yes':
        data = await state.get_data()  
        await task_service.TaskService().add_task(
            message.from_user.id, 
            **data
            )
        await message.answer(
            "Good. The task has been added",
            reply_markup=ReplyKeyboardRemove()
            )
    else:
        await message.answer(
            "Okey. Try to add task later",
            reply_markup=ReplyKeyboardRemove()
            )
    await state.clear()
        

@router.message(Command("view_tasks"))
async def view_all_tasks(message: Message):
    tasks = await task_service.TaskService().get_all_tasks(5, 0, message.from_user.id)
    msg = messages.all_tasks_message(tasks)
    keyboard = inline_kb_builder(
        'Previous',
        'Next', 
        callback_data='list_task')
    await message.answer(msg, reply_markup=keyboard)

@router.callback_query(F.data == 'list_task')
async def send_random(callback: CallbackQuery):
    await callback.message.answer("2")
    await callback.answer()

def get_tasks_range(start: int):
    return (start, start + 5)