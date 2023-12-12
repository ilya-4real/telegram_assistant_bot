from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from database.users import UsersRepository
from ..states import TaskForm


router = Router()


@router.message(Command("addtask"))
async def start_task_form(message: Message, state: FSMContext):
    user = await UsersRepository().get_one(message.from_user.id)
    if user[0].is_verified:
        await state.set_state(TaskForm.setting_title)
        await message.answer("The first step is the title of your task")
    else:
        await message.answer("You need to set your profile up")


@router.message(TaskForm.setting_title)
async def set_task_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(TaskForm.setting_body)
    await message.answer("Good! next step is the task body")


@router.message(TaskForm.setting_body)
async def set_task_body(message:Message, state: FSMContext):
    await state.update_data(body=message.text)
    await state.set_state(TaskForm.setting_expiration_date)
    await message.answer("Great, almost done! Enter the task expiration date")


@router.message(TaskForm.setting_expiration_date)
async def set_task_exp(message: Message, state: FSMContext):
    await state.update_data(exp_date=message.text)
    data = await state.get_data()
    print(data)
    await state.clear()
    await message.answer("Your task has been added to your task list")