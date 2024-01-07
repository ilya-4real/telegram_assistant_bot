from datetime import date, time, datetime, timedelta
import re


def days_to_datetime(days: int) -> date:
    """converts day to datetime format to python date"""
    result_date = datetime.today() + timedelta(days)
    return result_date.date()


def format_to_datetime(datetimeformat: str) -> date:
    """converts format like DD-MM-YY to python date"""
    day = int(datetimeformat[:2])
    month = int(datetimeformat[3:5])
    year = 2000 + int(datetimeformat[6:8])
    return date(year, month, day)


def check_date(date: str) -> date:
    """checks if the time entered correctly"""
    found = re.search(r"(^\d\d.\d\d.\d\d$)|(\d weeks?)|(\d days?)|(Today|today)", date)
    if not found:
        raise ValueError("Invalid date format")
    if found.groups()[0]:
        return format_to_datetime(found.groups()[0])
    elif found.groups()[1]:
        return days_to_datetime(int(found.group()[0]) * 7)
    elif found.groups()[2]:
        return days_to_datetime(int(found.group()[0]))
    elif found.group()[3]:
        return datetime.now().date()


def check_time(exp_time: str) -> time:
    """checks if the time entered correctly"""
    found = re.search(r"\d\d.\d\d", exp_time)
    if found:
        hours = int(found.group()[0:2])
        minutes = int(found.group()[3:5])
        return time(hours, minutes)
    raise ValueError("Invalid time format")
