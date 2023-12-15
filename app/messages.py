from aiogram.utils.markdown import text
from datetime import date, time

def common_message() -> str:
    msg = text(
        'Hello!',
        'I am your personal assistant.',
        'Now I can show you weather, currency rates and manage your tasks',
        sep='\n'
    )
    return msg

def getme_message(user_model) -> str:
    msg = text(
        "your saved on server data is:",
        f'user id : {user_model.id}',
        f'username : {user_model.username}',
        f'email : {user_model.email} ',
        f'verified: {user_model.is_verified}',
        f'date of registration : {user_model.registered_at}',
        sep='\n'
    )
    return msg


def check_task_message(title: str, body: str, exp_date: date, exp_time: time) -> str:
    day = str(exp_date)
    time = str(exp_time)
    msg = text(
        f"Title: {title}",
        f'Task info: {body}',
        f'Expires on {day} at {time}\n',
        'Is everything correct?',
        sep='\n'
    )
    return msg