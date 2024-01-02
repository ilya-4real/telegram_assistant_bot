from datetime import date, time, datetime, timedelta
import re


def weeks_n_days_to_datetime(days: int) -> date:
    result_date = datetime.today() + timedelta(days)
    return result_date.date()


def format_to_datetime(datetimeformat: str):
    date_list = datetimeformat.split('-')
    day = int(date_list[0])
    month = int(date_list[1])
    year = 2000 + int(date_list[2])
    return date(year, month, day)


def check_date(date: str):
    found = re.search(r'(\d\d.\d\d.\d\d)|(\d weeks?)|(\d days?)', date)
    if not found:
        raise ValueError("Invalid date format")
    if found.groups()[0]:
        return format_to_datetime(found.groups()[0])
    elif found.groups()[1]:
        return weeks_n_days_to_datetime(int(found.group()[0])*7)
    elif found.groups()[2]:
        return weeks_n_days_to_datetime(int(found.group()[0]))


def check_time(exp_time: str):
    found = re.search(r'\d\d.\d\d', exp_time)
    if found:
        hours = int(found.group()[0:2])
        minutes = int(found.group()[3:5])
        return time(hours, minutes)
    raise ValueError("Invalid time format")
