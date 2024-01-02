from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from .. import states
from services import check_date, check_time, TaskService, UsersService
from .. import messages
from ..keyboards import build_keyboard, task_detail_kb, tasks_kb, ask_to_delete_kb, TaskCallbackFactory
from config import TASKS_PAGE_SIZE

router = Router()


@router.message(Command("add_task"))
async def start_task_form(message: Message, state: FSMContext):
    user_verified = await UsersService.check_email(message.from_user.id)
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
            "Okey. Try to add task later",
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


@router.callback_query(F.data.startswith("prev_"))
@router.callback_query(F.data.startswith("next_"))
async def send_random(callback: CallbackQuery):
    tasks_start = int(callback.data.split("_")[1])
    await update_tasks(callback.message, tasks_start, callback.from_user.id)
    await callback.answer()


async def update_tasks(message: Message, page: int, user_id: int):
    start = page * TASKS_PAGE_SIZE
    tasks = await TaskService().get_all_tasks(int(TASKS_PAGE_SIZE), start, user_id)
    msg = messages.all_tasks_message(tasks)
    keyboard = tasks_kb(tasks, page)
    if tasks:
        await message.edit_text(text=msg, reply_markup=keyboard)
    else: 
        await message.edit_text('tasks are over...', reply_markup=keyboard)


@router.callback_query(F.data.startswith("taskdetail_"))
async def task_detail(callback: CallbackQuery):
    print(callback.data)
    task_id = int(callback.data.split('_')[1])
    task = await TaskService().get_task(task_id)
    msg = messages.task_detail(task)
    keyboard = task_detail_kb(task)
    await callback.message.edit_text(msg, reply_markup=keyboard)


@router.callback_query(TaskCallbackFactory.filter(F.action=='delete'))
async def task_action(callback: CallbackQuery, callback_data = TaskCallbackFactory):
    task_id = callback_data.task_id
    keyboard = ask_to_delete_kb(task_id)
    await callback.message.edit_text(
        f'Are you sure you want to delete this task?',
        reply_markup=keyboard
        )

@router.callback_query(TaskCallbackFactory.filter(F.action=='reallydelete'))
async def task_action(callback: CallbackQuery, callback_data = TaskCallbackFactory):
    task_id = callback_data.task_id
    await TaskService().delete_task(task_id)
    await callback.message.delete()


@router.callback_query(TaskCallbackFactory.filter(F.action=='notdelete'))
async def task_action(callback: CallbackQuery):
    await callback.message.delete()


@router.callback_query(TaskCallbackFactory.filter())
async def task_action(callback: CallbackQuery, callback_data = TaskCallbackFactory):
    action = callback_data.action
    match action:
        case 'title':
            ...
        case 'description':
            ...
        case 'date':
            ...
    await callback.message.edit_text(f'Well, send me new {action} for this task')

