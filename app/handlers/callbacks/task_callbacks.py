from aiogram import Router, F
from aiogram.filters.callback_data import CallbackData
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from app.states import states
from app.keyboards import keyboards
from app.messages import messages
from app.services import TaskService
from config import TASKS_PAGE_SIZE


router = Router()


class TaskCallbackFactory(CallbackData, prefix="task"):
    action: str
    task_id: int


@router.callback_query(F.data.startswith("prev_"))
@router.callback_query(F.data.startswith("next_"))
async def send_random(callback: CallbackQuery):
    tasks_start = int(callback.data.split("_")[1])
    await update_tasks(callback.message, tasks_start, callback.from_user.id)
    await callback.answer()


async def update_tasks(message: Message, page: int, user_id: int):
    start = page * TASKS_PAGE_SIZE
    tasks = await TaskService().get_all_tasks(TASKS_PAGE_SIZE, start, user_id)
    msg = messages.all_tasks_message(tasks)
    keyboard = keyboards.tasks_kb(tasks, page)
    if tasks:
        await message.edit_text(text=msg, reply_markup=keyboard)
    else:
        await message.edit_text(
            "No more tasks here. You can add some using /add_task",
            reply_markup=keyboard,
        )


@router.callback_query(F.data.startswith("taskdetail_"))
async def task_detail(callback: CallbackQuery):
    print(callback.data)
    task_id = int(callback.data.split("_")[1])
    task = await TaskService().get_task(task_id)
    msg = messages.task_detail(task)
    keyboard = keyboards.task_detail_kb(task)
    await callback.message.edit_text(msg, reply_markup=keyboard)


@router.callback_query(TaskCallbackFactory.filter(F.action == "delete"))
async def task_action(callback: CallbackQuery, callback_data=TaskCallbackFactory):
    task_id = callback_data.task_id
    keyboard = keyboards.ask_to_delete_kb(task_id)
    await callback.message.edit_text(
        f"Are you sure you want to delete this task?", reply_markup=keyboard
    )


@router.callback_query(TaskCallbackFactory.filter(F.action == "reallydelete"))
async def task_action(callback: CallbackQuery, callback_data=TaskCallbackFactory):
    task_id = callback_data.task_id
    await TaskService().delete_task(task_id)
    await callback.message.delete()


@router.callback_query(TaskCallbackFactory.filter(F.action == "notdelete"))
async def task_action(callback: CallbackQuery):
    await callback.message.delete()


@router.callback_query(TaskCallbackFactory.filter())
async def task_action(
    callback: CallbackQuery,
    state: FSMContext,
    callback_data=TaskCallbackFactory,
):
    action = callback_data.action
    match action:
        case "title":
            await state.set_state(states.TaskEditForm.editing_title)
        case "description":
            await state.set_state(states.TaskEditForm.editing_description)
        case "date":
            await state.set_state(states.TaskEditForm.editing_date)
    await state.update_data(task_id=callback_data.task_id)
    if action == "nothing":
        await callback.message.delete()
    else:
        await callback.message.edit_text(f"Well, send me new {action} for this task")
