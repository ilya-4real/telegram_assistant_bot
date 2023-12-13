from aiogram.fsm.state import StatesGroup, State


class UserState(StatesGroup):
    not_set = State()
    setting_city = State()
    setting_email = State()
    all_set = State()


class TaskForm(StatesGroup):
    setting_title = State()
    setting_body = State()
    setting_expiration_date = State()


class EmailForm(StatesGroup):
    setting_email = State()
    code_sent = State()
