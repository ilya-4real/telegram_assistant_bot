from dotenv import load_dotenv
import os


load_dotenv()

API_KEY = os.environ.get("API_KEY")
WEATHER_KEY = os.environ.get("WEATHER_API_KEY")
CURRENCIES_KEY = os.environ.get("CURRENCY_API_KEY")

SMTP_HOST = os.environ.get("SMTP_HOST")
SMTP_PORT = int(os.environ.get("SMTP_PORT"))
EMAIL_SENDER = os.environ.get("EMAIL_SENDER")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")

WEATHER_API_URL = os.environ.get("WEATHER_API_URL")
CURRENCIES_API_URL = os.environ.get("CURRENCIES_API_URL")

TASKS_PAGE_SIZE = int(os.environ.get("TASKS_PAGE_SIZE"))
