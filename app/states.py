from aiogram.fsm.state import StatesGroup, State


class TaskForm(StatesGroup):
    setting_title = State()
    setting_body = State()
    setting_exp_date = State()
    setting_exp_time = State()
    make_sure = State()


class TaskEditForm(StatesGroup):
    choosing_task = State()


class TaskDeleteForm(StatesGroup):
    choosing_task = State()
    delete_task = State()


class EmailForm(StatesGroup):
    setting_email = State()
    code_sent = State()


class CityForm(StatesGroup):
    setting_city = State()

class CurrencyForm(StatesGroup):
    setting_currency = State()
    make_sure = State()
