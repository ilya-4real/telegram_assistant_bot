from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from .. import states
from services import datetime_service, task_service, user_service
from .. import messages
from ..keyboards import build_keyboard, inline_kb_builder
from config import TASKS_PAGE_SIZE

router = Router()


@router.message(Command("add_task"))
async def start_task_form(message: Message, state: FSMContext):
    user_verified = await user_service.UsersService().check_email(message.from_user.id)
    if user_verified:
        await state.set_state(states.TaskForm.setting_title)
        await message.answer("The first step is the title of your task")
    else:
        await message.answer("You need to set email to your profile")


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
        date = datetime_service.check_date(message.text)
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
        time = datetime_service.check_time(message.text)
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
        

@router.message(Command("delete_task"))
async def on_delete_task(message: Message, state: FSMContext):
    await state.set_state(states.TaskDeleteForm.choosing_task)
    await message.answer("Okey. Send me the title of the task that you want to delete")


@router.message(states.TaskDeleteForm.choosing_task)
async def deleting_task(message: Message, state: FSMContext):
    task_title = message.text
    result = await task_service.TaskService().check_task(task_title)
    print(result)
    if result:
        keyboard = build_keyboard('Yes', 'No')
        await state.set_state(states.TaskDeleteForm.delete_task)
        await state.update_data(title=task_title)
        await message.answer("Are you sure?", reply_markup=keyboard)
    else:
        await message.answer("Task not found. Send the title again")


@router.message(states.TaskDeleteForm.delete_task)
async def delete_task(message: Message, state: FSMContext):
    if message.text == 'Yes':
        data = await state.get_data()
        await task_service.TaskService().delete_task(data['title'])
        await message.answer("The task has been deleted", reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer("Okey. I believe it's very important thing", reply_markup=ReplyKeyboardRemove())
        await state.clear()
    await state.clear()

@router.message(Command("edit_task"))
async def on_edit_task(message: Message, state: FSMContext):
    ...


@router.message(Command("view_tasks"))
async def view_all_tasks(message: Message):
    start_page = 0
    tasks = await task_service.TaskService().get_all_tasks(
        TASKS_PAGE_SIZE, 
        start_page, 
        message.from_user.id)
    msg = messages.all_tasks_message(tasks)
    keyboard = inline_kb_builder(start_page)
    await message.answer(msg, reply_markup=keyboard)


@router.callback_query(F.data.startswith("prev_"))
@router.callback_query(F.data.startswith("next_"))
async def send_random(callback: CallbackQuery):
    tasks_start = int(callback.data.split("_")[1])
    await update_tasks(callback.message, tasks_start, callback.from_user.id)
    await callback.answer()


async def update_tasks(message: Message, page: int, user_id: int):
    start = page * TASKS_PAGE_SIZE
    tasks = await task_service.TaskService().get_all_tasks(int(TASKS_PAGE_SIZE), start, user_id)
    msg = messages.all_tasks_message(tasks)
    keyboard = inline_kb_builder(page)
    if tasks:
        await message.edit_text(text=msg, reply_markup=keyboard)
    else: 
        await message.edit_text('tasks are over...', reply_markup=keyboard)