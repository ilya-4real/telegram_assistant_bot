from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from app.states import TaskEditForm, TaskForm
from app.services import (
    check_date,
    check_time,
    TaskService,
    UsersService,
)
from app.messages import check_task_message, all_tasks_message, task_dateformat_message
from app.keyboards import build_keyboard, tasks_kb
from app.config import TASKS_PAGE_SIZE

router = Router()

@router.message(Command("add_task"))
async def start_task_form(message: Message, state: FSMContext):
    user_verified = await UsersService.check_email(message.from_user.id)
    if user_verified:
        await state.set_state(TaskForm.setting_title)
        await message.answer("Firstly, send me your task title")
    else:
        await message.answer("You need to confirm your email /verify_email")


@router.message(TaskForm.setting_title)
async def set_task_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(TaskForm.setting_body)
    await message.answer("Good! next step is the task body")


@router.message(TaskForm.setting_body)
async def set_task_body(message: Message, state: FSMContext):
    await state.update_data(body=message.text)
    await state.set_state(TaskForm.setting_exp_date)
    msg = task_dateformat_message()
    await message.answer(msg)


@router.message(TaskForm.setting_exp_date)
async def set_task_date(message: Message, state: FSMContext):
    try:
        date = check_date(message.text)
        await state.update_data(exp_date=date)
        await state.set_state(TaskForm.setting_exp_time)
        await message.answer(
            "Date successfully set."
            " Send me exact time of expiration in format like HH-MM"
        )
    except ValueError as e:
        await message.answer(str(e))


@router.message(TaskForm.setting_exp_time)
async def set_task_time(message: Message, state: FSMContext):
    try:
        time = check_time(message.text)
        await state.update_data(exp_time=time)
        await state.set_state(TaskForm.make_sure)
        data = await state.get_data()
        keyboard = build_keyboard("Yes", "No")
        await message.answer(check_task_message(**data), reply_markup=keyboard)
    except ValueError as e:
        await message.answer(str(e))


@router.message(TaskForm.make_sure)
async def add_task(message: Message, state: FSMContext):
    if message.text == "Yes":
        data = await state.get_data()
        await TaskService().add_task(message.from_user.id, message, **data)
        await message.answer(
            "Good. The task has been added", reply_markup=ReplyKeyboardRemove()
        )
    else:
        await message.answer(
            "Okey. Try to add task again", reply_markup=ReplyKeyboardRemove()
        )
    await state.clear()


@router.message(Command("tasks"))
async def view_all_tasks(message: Message):
    start_page = 0
    tasks = await TaskService().get_all_tasks(
        TASKS_PAGE_SIZE, start_page, message.from_user.id
    )
    if tasks:
        msg = all_tasks_message(tasks)
        keyboard = tasks_kb(tasks, start_page)
        await message.answer(msg, reply_markup=keyboard)
    else:
        await message.answer("You have no tasks yet. Add some using /add_task command")

@router.message(TaskEditForm.editing_title)
async def update_task_title(message: Message, state: FSMContext):
    new_title = message.text
    state_data = await state.get_data()
    await TaskService().update_task_title(state_data["task_id"], title=new_title)
    await message.answer(f"Good, your task has been updated to {new_title}")


@router.message(TaskEditForm.editing_description)
async def update_task_description(message: Message, state: FSMContext):
    new_desc = message.text
    state_data = await state.get_data()
    await TaskService().update_task_desc(state_data["task_id"], description=new_desc)
    await message.answer("Good, your task has been updated")


@router.message(TaskEditForm.editing_date)
async def update_task_date(message: Message, state: FSMContext):
    new_date = message.text
    try:
        date = check_date(new_date)
        await state.update_data(new_date=date)
        await state.set_state(TaskEditForm.editing_time)
        await message.answer("Great, send me new expiration time in format like HH-MM")
    except ValueError as e:
        await message.answer(str(e))


@router.message(TaskEditForm.editing_time)
async def update_task_time(message: Message, state: FSMContext):
    new_time = message.text
    data = await state.get_data()
    try:
        time = check_time(new_time)
        await TaskService().reschedule_task(new_time=time, **data)
        await message.answer("Good, the task time has been updated")
    except ValueError as e:
        await message.answer(str(e))
    else:
        await state.clear()
