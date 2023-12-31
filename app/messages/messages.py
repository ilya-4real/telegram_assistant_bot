from aiogram.utils.markdown import text
from datetime import date, time

from app.database.models import Task, User
from app.APIs import ApisData


def welcome_message() -> str:
    msg = text(
        'Hello!',
        'I am your personal assistant.',
        'First of all, you need to setup your profile',
        '1. Confirm your email(/verify_email) for all services',
        '2. Set your city(/set_city) for weather service',
        '3. Set preferred currency symbols(/add_currency) for rates service',
        'By the way you can send me any message and I will show you a little help message',
        sep='\n'
    )
    return msg

def common_message() -> str:
    """creates message for all unhandled messages"""
    msg = text(
        'Hi there!',
        'I am your personal assistant',
        'I can show you weather /weather',
        'currency rates /currency',
        'and manage your tasks /tasks',
        "if you're stuck use /dropstate",
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


def task_detail(task: Task):
    msg = text(
        f'title: {task.title}',
        f'description: {task.body}',
        f'expires: {task.expires_at}\n',
        'What would you like to change?', 
        sep='\n'
    )
    return msg


def weather_message(weather: dict) -> str:
    """creates message for weather"""
    msg = text(
        '<b>Current weather</b>\n',
        f'Description: {weather['weather'][0]['description']}',
        f'Temperature: {weather['main']['temp']}',
        f'Feels like: {weather['main']['feels_like']}',
        f'Pressure: {weather['main']['pressure']}',
        f'Wind speed: {weather['wind']['speed']}',
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

def task_dateformat_message() -> str:
    """returns date format help message"""
    msg = text(
        'Send me exact date of expiration in format DD-MM-YY or using human language today | 1 week | 2 days.'
        ' I will notify you when the deadline approaches'
    )
    return msg


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
