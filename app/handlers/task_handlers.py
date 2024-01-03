from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from .. import states
from services import check_date, check_time, TaskService, UsersService
from .. import messages
from ..keyboards import build_keyboard, tasks_kb
from config import TASKS_PAGE_SIZE

router = Router()


@router.message(Command("add_task"))
async def start_task_form(message: Message, state: FSMContext):
    user_verified = await UsersService.check_email(message.from_user.id)
    if user_verified:
        await state.set_state(states.TaskForm.setting_title)
        await message.answer("Firstly, send me your task title")
    else:
        await message.answer("You need to confirm your email /verify_email")


@router.message(states.TaskForm.setting_title)
async def set_task_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(states.TaskForm.setting_body)
    await message.answer("Good! next step is the task body")


@router.message(states.TaskForm.setting_body)
async def set_task_body(message:Message, state: FSMContext):
    await state.update_data(body=message.text)
    await state.set_state(states.TaskForm.setting_exp_date)
    await message.answer(
        "Great, almost done! Enter the task expiration date"
        " in format like dd-mm-yy"
        )


@router.message(states.TaskForm.setting_exp_date)
async def set_task_date(message: Message, state: FSMContext):
    try:
        date = check_date(message.text)
        await state.update_data(exp_date=date)
        await state.set_state(states.TaskForm.setting_exp_time)
        await message.answer(
            "Date successfully set."
            " Send me exact time of expiration in format like hh-mm"
            )
    except ValueError as e:
        await message.answer(str(e))
    

@router.message(states.TaskForm.setting_exp_time)
async def set_task_time(message: Message, state: FSMContext):
    try:
        time = check_time(message.text)
        await state.update_data(exp_time=time)
        await state.set_state(states.TaskForm.make_sure)
        data = await state.get_data()
        keyboard = build_keyboard('Yes', 'No')
        await message.answer(
            messages.check_task_message(**data),
            reply_markup=keyboard
            )
    except ValueError as e:
         await message.answer(str(e))


@router.message(states.TaskForm.make_sure)
async def add_task(message: Message, state: FSMContext):
    if message.text == 'Yes':
        data = await state.get_data()  
        await TaskService().add_task(
            message.from_user.id, 
            **data
            )
        await message.answer(
            "Good. The task has been added",
            reply_markup=ReplyKeyboardRemove()
            )
    else:
        await message.answer(
            "Okey. Try to add task again",
            reply_markup=ReplyKeyboardRemove()
            )
    await state.clear()


@router.message(Command("tasks"))
async def view_all_tasks(message: Message):
    start_page = 0
    tasks = await TaskService().get_all_tasks(
        TASKS_PAGE_SIZE, 
        start_page, 
        message.from_user.id
        )
    msg = messages.all_tasks_message(tasks)
    keyboard = tasks_kb(tasks, start_page)
    await message.answer(msg, reply_markup=keyboard)


@router.message(states.TaskEditForm.editing_title)
async def update_task_title(message: Message, state: FSMContext):
    new_title = message.text
    state_data = await state.get_data()
    await TaskService().update_task(state_data['task_id'], title=new_title)
    await message.answer("Good, your task has been updated")


@router.message(states.TaskEditForm.editing_description)
async def update_task_title(message: Message, state: FSMContext):
    new_desc = message.text
    state_data = await state.get_data()
    await TaskService().update_task(state_data['task_id'], body=new_desc)
    await message.answer("Good, your task has been updated")


@router.message(states.TaskEditForm.editing_date)
async def update_task_title(message: Message, state: FSMContext):
    new_date = message.text
    state_data = await state.get_data()
    try:
        date = check_date(new_date)
        await state.update_data(date=date)
        await state.set_state(states.TaskEditForm.editing_time)
        await message.answer("Great, send me new expiration time in format like HH-MM")
    except ValueError as e:
        await message.answer(str(e))
    

@router.message(states.TaskEditForm.editing_time)
async def update_task_title(message: Message, state: FSMContext):
    new_time = message.text
    state_data = await state.get_data()
    try:
        time = check_time(new_time)
        new_date = state_data['date']
        exp_datetime = TaskService.combine_date_time(new_date, time)
        await TaskService().update_task(state_data['task_id'], expires_at=exp_datetime)
        await message.answer("Good, your task has been updated")
    except ValueError as e:
        await message.answer(str(e))