from dotenv import load_dotenv
import os


load_dotenv()

API_KEY = os.environ.get("API_KEY")
WEATHER_KEY = os.environ.get("WEATHER_API_KEY")
CURRENCIES_KEY = os.environ.get("CURRENCY_API_KEY")

SMTP_HOST = 'smtp.gmail.com'
SMTP_PORT = 465
EMAIL_SENDER = os.environ.get("EMAIL_SENDER")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")

WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"
CURRENCIES_API_URL = "http://api.exchangeratesapi.io/v1/latest"

TASKS_PAGE_SIZE = 5
