from aiogram.utils.markdown import text
from datetime import date, time
from database.models import Task, User
from APIs import ApisData


def common_message() -> str:
    """creates message for all unhandled messages"""
    msg = text(
        'Hello!',
        'I am your personal assistant.',
        'Now I can show you weather, currency rates and manage your tasks',
        sep='\n'
    )
    return msg


def getme_message(user_model: User, currency_symbols: str) -> str:
    """creates message for user data"""
    msg = text(
        "your saved on server data is:",
        f'user id : {user_model.id}',
        f'username : {user_model.username}',
        f'email : {user_model.email} ',
        f'city : {user_model.city} ',
        f'currencies: {currency_symbols}',
        f'date of registration : {user_model.registered_at}',
        sep='\n'
    )
    return msg


def check_task_message(title: str, body: str, exp_date: date, exp_time: time) \
     -> str:
    """creates message to check task data"""
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


def all_tasks_message(tasks: list[Task]) -> str:
    """creates message for listing tasks"""
    list_of_strings = []
    for task in tasks:
        list_of_strings.extend(
            [f'<b>{task.title}\n{task.body[:20]}</b>', f'{task.expires_at}\n']
            )
    result = text(*list_of_strings, sep='\n')
    return result


def weather_message(weather: dict) -> str:
    """creates message for weather"""
    msg = text(
        '<b>Current weather</b>',
        f'temperature: {weather['main']['temp']}',
        f'feels like: {weather['main']['feels_like']}',
        f'pressure: {weather['main']['pressure']}',
        f'wind speed: {weather['wind']['speed']}',
        sep='\n'
    )
    return msg


def get_cur_message(rates: dict[str, float]) -> str:
    """creates message for currency rates"""
    list_of_curs = []
    for i, k in rates.items():
        list_of_curs.append(f'{i} : {k}')
    return text(
        '<b>Currency rates for today</b>',
        *list_of_curs,
        sep='\n'
        )


def todays_info_message(data: ApisData) -> str:
    """creates message combined of weather and currency rates"""
    weather_msg = weather_message(data.weather)
    cur_msg = get_cur_message(data.currency)
    msg = text(
        weather_msg,
        cur_msg,
        sep='\n'
    )
    return msg