from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from database.users import UsersRepository
from ..states import TaskForm
from services.task_date_checking import check_date, check_time
from ..messages import check_task_message
from database.services.task_service import TaskService


router = Router()


@router.message(Command("addtask"))
async def start_task_form(message: Message, state: FSMContext):
    # user = await UsersRepository().get_one(message.from_user.id)
    # if user[0].is_verified:
        await state.set_state(TaskForm.setting_title)
        await message.answer("The first step is the title of your task")
    # else:
    #     await message.answer("You need to set your profile up")


@router.message(TaskForm.setting_title)
async def set_task_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(TaskForm.setting_body)
    await message.answer("Good! next step is the task body")


@router.message(TaskForm.setting_body)
async def set_task_body(message:Message, state: FSMContext):
    await state.update_data(body=message.text)
    await state.set_state(TaskForm.setting_exp_date)
    await message.answer("Great, almost done! Enter the task expiration date")


@router.message(TaskForm.setting_exp_date)
async def set_task_date(message: Message, state: FSMContext):
    try:
        date = check_date(message.text)
        await state.update_data(date=date)
        await state.set_state(TaskForm.setting_exp_time)
        await message.answer("Date successfully set")
    except ValueError as e:
        await message.answer(str(e))
    

@router.message(TaskForm.setting_exp_time)
async def set_task_time(message: Message, state: FSMContext):
    try:
        time = check_time(message.text)
        await state.update_data(time=time)
        await state.set_state(TaskForm.make_sure)
        data = await state.get_data()
        await message.answer(
             check_task_message(
                  data['title'], 
                  data['body'], 
                  data['date'], 
                  data['time'])
            )
    except ValueError as e:
         await message.answer(e)


@router.message(TaskForm.make_sure)
async def add_task(message: Message, state: FSMContext):
     if message.text == 'yes':
        data = await state.get_data()  
        await TaskService().add_task(
            message.from_user.id, 
            data['title'],
            data['body'],
            data['date'],
            data['time']
            )
        

@router.message(Command("view_tasks"))
async def view_all_tasks(message: Message):
    tasks = await TaskService().get_all()
    print(tasks)
    await message.answer("Done")
