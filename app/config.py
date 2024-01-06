from dotenv import load_dotenv
import os


load_dotenv()

API_KEY = os.environ.get("API_KEY")
ADMIN_ID = os.environ.get("ADMIN_ID")
WEATHER_KEY = os.environ.get("WEATHER_API_KEY")
CURRENCIES_KEY = os.environ.get("CURRENCY_API_KEY")

SMTP_HOST = os.environ.get("SMTP_HOST")
SMTP_PORT = int(os.environ.get("SMTP_PORT"))
EMAIL_SENDER = os.environ.get("EMAIL_SENDER")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")

WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"
CURRENCIES_API_URL = "http://api.exchangeratesapi.io/v1/latest"

LOCAL_IP = os.environ.get("LOCAL_IP")

TASKS_PAGE_SIZE = int(os.environ.get("TASKS_PAGE_SIZE"))
